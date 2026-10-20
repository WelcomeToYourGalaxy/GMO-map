#!/usr/bin/env python3
"""Globe, round 2:
  - basemaps (Jurassic, Atlas, Bioluminescent, Hell, Standard) on the flat map too
  - the flat map drags freely past its edges
  - the globe shows everything the flat map draws: country outlines and
    highlights, regime outlines, shaded areas, international-body markers
  - the view box moves to the top right and drives both maps
  - Hologram removed

Run from the repo root, after patch_globe.py:  python3 patch_globe_2.py
Applies by exact-text match, refuses to run twice, exits 0 when already done.
"""
import pathlib, sys

BLOCK = r"""<!-- =====================================================================
     THE GLOBE. The map opens as a planet (MapLibre, vertical-perspective
     projection). It carries what the flat map draws: the record markers, the
     country outlines and highlights, the regime outlines, the shaded areas
     and the international-body markers, copied from the flat map as they
     stand and kept in step as filters change. "Flat map" is the Leaflet map.
     The basemaps from the Culprits atlas - Jurassic, Atlas, Bioluminescent,
     Hell, Standard - work in both views; on the flat map all but Atlas are
     drawn by MapLibre inside Leaflet. Everything here lives between these two
     comment bars.
     ====================================================================== -->
<link rel="stylesheet" href="https://unpkg.com/maplibre-gl@5.24.0/dist/maplibre-gl.css">
<script src="https://unpkg.com/maplibre-gl@5.24.0/dist/maplibre-gl.js"></script>
<script src="https://unpkg.com/@maplibre/maplibre-gl-leaflet@0.1.3/leaflet-maplibre-gl.js"></script>
<style id="globe-style">
  #globe{position:absolute;left:0;top:0;width:100%;height:100vh;z-index:900;background:#040611;
    transition:opacity .35s ease;}
  #globe.off{opacity:0;pointer-events:none;visibility:hidden;}
  #globe .maplibregl-canvas-container,#globe .maplibregl-canvas{outline:none;}
  #globeStars{position:absolute;inset:0;width:100%;height:100%;pointer-events:none;}
  #globeMap{position:absolute;inset:0;}
  body.globe-on #map{visibility:hidden;}
  body.globe-on #gbCrumb{display:none!important;}
  /* The flat map's own zoom and world buttons: the view box does both jobs. */
  #map .leaflet-top.leaflet-left{display:none!important;}
  #globeTip{position:absolute;z-index:3;pointer-events:none;display:none;max-width:260px;padding:5px 9px;
    background:rgba(8,12,27,0.95);border:1px solid var(--accent-soft);border-radius:7px;color:#e3e6ef;
    font-size:11.5px;line-height:1.35;box-shadow:0 3px 14px rgba(0,0,0,.5);}
  #globeTip b{display:block;color:#f0ece4;font-weight:600;}
  #globeTip span{color:#969eb1;}
  /* The view box, top right, above the Guides column. */
  #globeBox{position:fixed;right:16px;top:10px;z-index:1300;display:flex;align-items:center;
    gap:8px;padding:5px 8px;background:rgba(8,12,27,0.95);border:1px solid var(--accent-soft);border-radius:10px;
    backdrop-filter:blur(10px);box-shadow:0 4px 22px rgba(0,0,0,0.45);font-family:'Marcellus','Georgia',serif;
    font-size:12px;color:#d6dae8;max-width:calc(100vw - 300px);flex-wrap:wrap;justify-content:flex-end;}
  #globeBox .gb-grp{display:flex;align-items:center;gap:4px;}
  #globeBox .gb-cap{font-size:9.5px;letter-spacing:.6px;text-transform:uppercase;color:#8a93ad;margin-right:2px;}
  #globeBox button{font:inherit;font-size:12px;color:#d6dae8;background:rgba(20,27,56,0.55);border:1px solid var(--accent-soft);
    border-radius:7px;padding:4px 8px;cursor:pointer;line-height:1.15;white-space:nowrap;}
  #globeBox button:hover{background:rgba(34,46,98,0.75);color:#fff;}
  #globeBox button.on{background:#2e3e72;color:#fff;border-color:#4e62a8;}
  #globeBox .gb-zoom button{width:28px;padding:4px 0;font-size:15px;font-weight:700;}
  #globeBox .gb-sep{width:1px;height:26px;background:var(--accent-soft);}
  #globeBox .gb-sub{display:block;font-size:9px;color:#8a93ad;letter-spacing:.2px;margin-top:1px;}
  #globeBox button.bm{text-align:center;padding:3px 7px;}
  #globeBox button.bm.on .gb-sub{color:#c9d1ee;}
  @media (max-width:900px){ #globeBox{top:6px;right:8px;max-width:calc(100vw - 16px);gap:5px;} #globeBox .gb-sub{display:none;} }
</style>
<script id="globe-script">
(function(){
  "use strict";
  if(typeof maplibregl==="undefined"||!maplibregl.Map){ console.warn("[globe] MapLibre did not load; the flat map stands alone."); return; }
  var mapEl=document.getElementById("map"); if(!mapEl) return;

  /* ---------- the page: a container after the flat map, and the view box ---------- */
  var box=document.createElement("div"); box.id="globe";
  box.innerHTML='<canvas id="globeStars"></canvas><div id="globeMap"></div><div id="globeTip"></div>';
  mapEl.parentNode.insertBefore(box, mapEl.nextSibling);

  // The basemaps as the Culprits atlas names them, with a word for a reader
  // who has never seen them. Woodlands and Hologram are left out at the
  // owner's word.
  var BASEMAPS=[
    ["jurassic","Jurassic","photo + relief","The satellite photograph of Earth with shaded relief laid over it in earth tones."],
    ["atlas","Atlas","painted chart","The painted world chart. Zoom in and it gives way to the photograph underneath."],
    ["night","Bioluminescent","Earth at night","NASA's picture of the planet's lights after dark, in navy and ice, with a glow along every shore."],
    ["hell","Hell","oxblood, basalt","The same Earth drawn in oxblood sea, black land and red rivers."],
    ["outlines","Standard","plain outlines","Plain country shapes on dark water, with roads, rivers and buildings close in."]];
  var BM_KEY="gmo-globe-basemap";
  var BASEMAP="atlas";
  try{ var kept=localStorage.getItem(BM_KEY); if(kept&&BASEMAPS.some(function(b){return b[0]===kept;})) BASEMAP=kept; }catch(e){}

  var ctl=document.createElement("div"); ctl.id="globeBox";
  ctl.innerHTML=
    '<div class="gb-grp"><span class="gb-cap">View</span>'+
      '<button type="button" id="gbViewGlobe" class="on" title="The planet, turning">Globe</button>'+
      '<button type="button" id="gbViewFlat" title="The flat map, with every panel and filter">Flat map</button></div>'+
    '<div class="gb-sep"></div>'+
    '<div class="gb-grp" id="gbBasemaps"><span class="gb-cap">Basemap</span>'+
      BASEMAPS.map(function(b){ return '<button type="button" class="bm'+(b[0]===BASEMAP?" on":"")+'" data-bm="'+b[0]+'" title="'+b[3]+'">'+b[1]+'<span class="gb-sub">'+b[2]+'</span></button>'; }).join("")+'</div>'+
    '<div class="gb-sep"></div>'+
    '<div class="gb-grp gb-zoom"><button type="button" id="gbZoomIn" title="Zoom in">+</button><button type="button" id="gbZoomOut" title="Zoom out">&minus;</button></div>'+
    '<button type="button" id="gbWorld" title="Zoom back out until the whole planet is in view">Back to world view</button>';
  document.body.appendChild(ctl);

  /* ---------- stars behind the planet ---------- */
  var stars=document.getElementById("globeStars");
  function drawStars(){
    var w=box.clientWidth,h=box.clientHeight; if(!w||!h) return;
    stars.width=w; stars.height=h;
    var g=stars.getContext("2d"); g.clearRect(0,0,w,h);
    var s=1234567; var rnd=function(){ s=(s*16807)%2147483647; return s/2147483647; };
    var n=Math.round(w*h/3800);
    for(var i=0;i<n;i++){ var x=rnd()*w,y=rnd()*h,r=rnd(); g.fillStyle="rgba(220,228,255,"+(0.15+r*r*0.6).toFixed(2)+")"; g.beginPath(); g.arc(x,y,r<0.9?0.6:1.1,0,Math.PI*2); g.fill(); }
  }
  drawStars(); window.addEventListener("resize",drawStars);

  /* ---------- helpers ported from the Culprits atlas ---------- */
  var PLATE={ top:85.05112877980659, bot:-80.55, fadeIn:3, fadeOut:5 };
  function pngCrc(buf,start,end){
    var c=~0; for(var i=start;i<end;i++){ c^=buf[i]; for(var k=0;k<8;k++) c=(c>>>1)^(0xEDB88320&-(c&1)); } return ~c>>>0; }
  function rawPng(rgba,w,h){
    var row=w*4+1, raw=row*h, blocks=Math.ceil(raw/65535);
    var zlen=2+raw+blocks*5+4;
    var out=new Uint8Array(8+25+(12+zlen)+12);
    var dv=new DataView(out.buffer);
    out.set([137,80,78,71,13,10,26,10],0);
    var o=8;
    var chunk=function(type,len,fill){
      dv.setUint32(o,len); o+=4; var start=o;
      for(var i=0;i<4;i++) out[start+i]=type.charCodeAt(i);
      fill(start+4); o=start+4+len;
      dv.setUint32(o,pngCrc(out,start,o)); o+=4; };
    chunk("IHDR",13,function(at){ dv.setUint32(at,w); dv.setUint32(at+4,h); out.set([8,6,0,0,0],at+8); });
    chunk("IDAT",zlen,function(at){
      var q=at; out[q++]=0x78; out[q++]=0x01;
      var a1=1,a2=0,left=raw,i=0;
      while(left>0){ var n=Math.min(65535,left); left-=n;
        out[q++]=left===0?1:0; out[q++]=n&255; out[q++]=n>>8; out[q++]=~n&255; out[q++]=(~n>>8)&255;
        for(var k=0;k<n;k++,i++){ var y=(i/row)|0, x=i-y*row; var v=x===0?0:rgba[y*w*4+x-1]; out[q++]=v; a1=(a1+v)%65521; a2=(a2+a1)%65521; } }
      dv.setUint32(q,((a2<<16)|a1)>>>0); });
    chunk("IEND",0,function(){});
    return out.buffer; }
  function hexRgb(h){ var n=parseInt(h.slice(1),16); return [(n>>16&255)/255,(n>>8&255)/255,(n&255)/255]; }
  var cv256=function(w,h){ return typeof OffscreenCanvas!=="undefined"?new OffscreenCanvas(w,h):Object.assign(document.createElement("canvas"),{width:w,height:h}); };

  /* ---------- Earth at night, recoloured square by square ---------- */
  var NIGHT={
    tiles:"https://gibs.earthdata.nasa.gov/wmts/epsg3857/best/VIIRS_Black_Marble/default/2016-01-01/GoogleMapsCompatible_Level8/{z}/{y}/{x}.png",
    ramp:[[0,"#02040C"],[14,"#050918"],[34,"#0B1430"],[62,"#17295A"],[100,"#2E5390"],[145,"#5E8DC2"],[190,"#A5C7E2"],[230,"#DCE8F0"],[255,"#F1F4F6"]],
    sheet:"#02040C",
    shade:{"hillshade-method":"multidirectional","hillshade-illumination-direction":[315,270,0,225],"hillshade-illumination-altitude":[35,30,30,45],
      "hillshade-highlight-color":["rgba(170,196,230,0.12)","rgba(170,196,230,0.05)","rgba(170,196,230,0.05)","rgba(170,196,230,0.03)"],
      "hillshade-shadow-color":["rgba(0,1,6,0.45)","rgba(0,1,6,0.25)","rgba(0,1,6,0.25)","rgba(0,1,6,0.15)"],
      "hillshade-accent-color":"rgba(0,1,6,0.15)","hillshade-exaggeration":0.8,"hillshade-illumination-anchor":"map"},
    road:["rgba(150,186,222,0.30)","rgba(170,202,232,0.45)","rgba(206,226,240,0.70)"], roadGlow:"#2D5C96",
    seaGlow:["interpolate",["linear"],["elevation"],-9000,"rgba(31,79,126,0)",-150,"rgba(31,79,126,0)",-60,"rgba(31,79,126,0.28)",-15,"rgba(31,79,126,0.55)",-3,"rgba(74,154,182,0.85)",0,"rgba(74,154,182,0)",9000,"rgba(74,154,182,0)"],
    border:"rgba(120,140,196,0.32)",
    sky:{"sky-color":"#02030A","horizon-color":"#1C3566","fog-color":"#0B1630","fog-ground-blend":0.9,"horizon-fog-blend":0.3,"sky-horizon-blend":0.6,
      "atmosphere-blend":["interpolate",["linear"],["zoom"],0,0.55,4,0.3,7,0]} };
  var NIGHT_TABLE=null;
  function nightTable(){ var hex=function(h){ return [1,3,5].map(function(i){ return parseInt(h.slice(i,i+2),16); }); };
    var t=new Uint8Array(256*3), R=NIGHT.ramp;
    for(var v=0;v<256;v++){ var k=0; while(k<R.length-2&&v>R[k+1][0]) k++;
      var v0=R[k][0],c0=R[k][1],v1=R[k+1][0],c1=R[k+1][1];
      var f=Math.max(0,Math.min(1,(v-v0)/(v1-v0))), a=hex(c0), b=hex(c1);
      for(var i=0;i<3;i++) t[v*3+i]=Math.round(a[i]+(b[i]-a[i])*f); }
    return t; }
  maplibregl.addProtocol("gmonight", function(params, ac){
    var m=params.url.match(/^gmonight:\/\/(\d+)\/(\d+)\/(\d+)$/); if(!m) return Promise.reject(new Error("not a night square"));
    var url=NIGHT.tiles.replace("{z}",m[1]).replace("{y}",m[2]).replace("{x}",m[3]);
    return fetch(url, ac&&ac.signal?{signal:ac.signal}:undefined).then(function(r){ if(!r.ok) throw new Error("GIBS "+r.status); return r.blob(); })
      .then(function(b){ return createImageBitmap(b); }).then(function(img){
        var w=img.width,h=img.height, cv=cv256(w,h), ctx=cv.getContext("2d"); ctx.drawImage(img,0,0);
        var d=ctx.getImageData(0,0,w,h), px=d.data; if(!NIGHT_TABLE) NIGHT_TABLE=nightTable();
        for(var i=0;i<px.length;i+=4){ var r=px[i],g=px[i+1],bl=px[i+2];
          var v=Math.round(0.5*Math.max(r,g,bl)+0.5*(0.3*r+0.59*g+0.11*bl));
          px[i]=NIGHT_TABLE[v*3]; px[i+1]=NIGHT_TABLE[v*3+1]; px[i+2]=NIGHT_TABLE[v*3+2]; px[i+3]=255; }
        return {data:rawPng(px,w,h)}; }); });

  /* ---------- the atlas's colour washes, as one WebGL layer ---------- */
  var ATLAS_TUNE={sat:.15,con:.05,lift:.03,hue:-6,sea:.55,green:.30,warm:.22};
  var BASE_GRADE={
    atlas:{"raster-brightness-min":ATLAS_TUNE.lift,"raster-brightness-max":1,"raster-saturation":ATLAS_TUNE.sat,"raster-contrast":ATLAS_TUNE.con,"raster-hue-rotate":ATLAS_TUNE.hue},
    jurassic:{"raster-brightness-min":0.02,"raster-brightness-max":0.92,"raster-saturation":0.12,"raster-contrast":0.06,"raster-hue-rotate":0} };
  function atlasWashPasses(z){
    var t=z<=6?1:z>=13?0.45:1-(z-6)*(0.55/7), sea=z<=6?1:0.7, passes=[];
    var aSea=ATLAS_TUNE.sea*sea; passes.push({mode:"screen",rgb:hexRgb("#0f3b52").map(function(c){ return c*aSea; })});
    var aG=ATLAS_TUNE.green*t; passes.push({mode:"multiply",rgb:hexRgb("#5f8f3a").map(function(c){ return 1-aG*(1-(c<.5?.5+c:1)); })});
    var aW=ATLAS_TUNE.warm*t, warm=hexRgb("#f0c073");
    passes.push({mode:"gain",rgb:warm.map(function(c){ return c>.5?aW*(2*c-1):0; })});
    passes.push({mode:"multiply",rgb:warm.map(function(c){ return c<.5?1-aW*(1-2*c):1; })});
    return passes; }
  function washMesh(cols,rows){ var v=[];
    for(var j=0;j<rows;j++){ var y0=j/rows,y1=(j+1)/rows; for(var i=0;i<cols;i++){ var x0=i/cols,x1=(i+1)/cols; v.push(x0,y0,x1,y0,x0,y1,x1,y0,x1,y1,x0,y1); } }
    return new Float32Array(v); }
  var atlasWashes={ id:"atlas-washes", type:"custom", renderingMode:"2d",
    onAdd:function(m,gl){ this.map=m; this.programs={};
      try{ this.mesh=washMesh(96,64); this.buf=gl.createBuffer(); gl.bindBuffer(gl.ARRAY_BUFFER,this.buf); gl.bufferData(gl.ARRAY_BUFFER,this.mesh,gl.STATIC_DRAW); }
      catch(e){ this.failed=true; console.warn("[globe] atlas washes unavailable:",e.message||e); } },
    program:function(gl,sd){ var key=sd.variantName; if(this.programs[key]) return this.programs[key];
      var sh=function(type,src){ var o=gl.createShader(type); gl.shaderSource(o,src); gl.compileShader(o);
        if(!gl.getShaderParameter(o,gl.COMPILE_STATUS)) throw new Error(gl.getShaderInfoLog(o)); return o; };
      var p=gl.createProgram();
      gl.attachShader(p,sh(gl.VERTEX_SHADER,"#version 300 es\n"+sd.vertexShaderPrelude+"\n"+sd.define+"\nin vec2 a_pos;\nvoid main() { gl_Position = projectTile(a_pos); }"));
      gl.attachShader(p,sh(gl.FRAGMENT_SHADER,"#version 300 es\nprecision mediump float;\nuniform vec3 c;\nout vec4 colour;\nvoid main() { colour = vec4(c, 1.0); }"));
      gl.linkProgram(p); if(!gl.getProgramParameter(p,gl.LINK_STATUS)) throw new Error(gl.getProgramInfoLog(p));
      var u=function(n){ return gl.getUniformLocation(p,n); };
      var prog={p:p,aPos:gl.getAttribLocation(p,"a_pos"),uCol:u("c"),uMatrix:u("u_projection_matrix"),uFallback:u("u_projection_fallback_matrix"),
        uTile:u("u_projection_tile_mercator_coords"),uClip:u("u_projection_clipping_plane"),uTransition:u("u_projection_transition")};
      this.programs[key]=prog; return prog; },
    render:function(gl,options){
      if(this.failed||BASEMAP!=="atlas"||!options||!options.shaderData) return;
      var prog; try{ prog=this.program(gl,options.shaderData); }catch(e){ this.failed=true; console.warn("[globe] atlas washes unavailable:",e.message||e); return; }
      if(gl.bindVertexArray) gl.bindVertexArray(null);
      gl.disable(gl.DEPTH_TEST); gl.disable(gl.STENCIL_TEST); gl.disable(gl.CULL_FACE);
      gl.useProgram(prog.p); var d=options.defaultProjectionData;
      if(prog.uMatrix) gl.uniformMatrix4fv(prog.uMatrix,false,d.mainMatrix);
      if(prog.uFallback) gl.uniformMatrix4fv(prog.uFallback,false,d.fallbackMatrix);
      if(prog.uTile) gl.uniform4f(prog.uTile,d.tileMercatorCoords[0],d.tileMercatorCoords[1],d.tileMercatorCoords[2],d.tileMercatorCoords[3]);
      if(prog.uClip) gl.uniform4f(prog.uClip,d.clippingPlane[0],d.clippingPlane[1],d.clippingPlane[2],d.clippingPlane[3]);
      if(prog.uTransition) gl.uniform1f(prog.uTransition,d.projectionTransition);
      gl.bindBuffer(gl.ARRAY_BUFFER,this.buf); gl.enableVertexAttribArray(prog.aPos); gl.vertexAttribPointer(prog.aPos,2,gl.FLOAT,false,0,0);
      gl.enable(gl.BLEND);
      var func={screen:[gl.ONE,gl.ONE_MINUS_SRC_COLOR],multiply:[gl.ZERO,gl.SRC_COLOR],gain:[gl.DST_COLOR,gl.ONE]};
      var count=this.mesh.length/2, passes=atlasWashPasses(this.map.getZoom());
      for(var i=0;i<passes.length;i++){ var f=func[passes[i].mode]; gl.blendFuncSeparate(f[0],f[1],gl.ZERO,gl.ONE);
        gl.uniform3f(prog.uCol,passes[i].rgb[0],passes[i].rgb[1],passes[i].rgb[2]); gl.drawArrays(gl.TRIANGLES,0,count); } } };

  /* ---------- sources shared by the basemaps ---------- */
  var OSM_SOURCE={type:"vector",url:"https://tiles.openfreemap.org/planet",attribution:'<a href="https://openfreemap.org" target="_blank" rel="noopener">OpenFreeMap</a> © OpenStreetMap contributors'};
  var RELIEF_SOURCE={type:"raster-dem",tiles:["https://tiles.mapterhorn.com/{z}/{x}/{y}.webp"],encoding:"terrarium",tileSize:512,maxzoom:12,attribution:'<a href="https://mapterhorn.com/attribution" target="_blank" rel="noopener">© Mapterhorn</a>'};
  var TERRAIN_SOURCE={type:"raster-dem",tiles:["https://s3.amazonaws.com/elevation-tiles-prod/terrarium/{z}/{x}/{y}.png"],encoding:"terrarium",tileSize:256,maxzoom:12,attribution:'<a href="https://registry.opendata.aws/terrain-tiles/" target="_blank" rel="noopener">AWS Terrain Tiles</a>'};
  var WORLD_SHEET={type:"geojson",data:{type:"Feature",properties:{},geometry:{type:"Polygon",coordinates:[[[-180,-85.06],[180,-85.06],[180,85.06],[-180,85.06],[-180,-85.06]]]}}};
  var SAT_RELIEF={
    colour:["interpolate",["linear"],["elevation"],-8000,"rgba(10,22,42,0.8)",-3500,"rgba(12,28,50,0.72)",-1200,"rgba(16,40,60,0.6)",-200,"rgba(26,70,86,0.38)",-40,"rgba(40,96,102,0.22)",0,"rgba(40,90,90,0.1)",
      1,"rgba(46,52,34,0.32)",400,"rgba(48,54,36,0.3)",1000,"rgba(64,70,44,0.28)",1700,"rgba(108,100,66,0.26)",2500,"rgba(118,90,60,0.3)",3300,"rgba(110,80,62,0.32)",4300,"rgba(102,92,84,0.3)",5500,"rgba(132,128,122,0.2)"],
    seabed:["interpolate",["linear"],["elevation"],-8000,"rgba(10,22,42,0.8)",-3500,"rgba(12,28,50,0.72)",-1200,"rgba(16,40,60,0.6)",-200,"rgba(26,70,86,0.38)",-40,"rgba(40,96,102,0.22)",-1,"rgba(40,90,90,0.1)",0,"rgba(0,0,0,0)"],
    sea:["interpolate",["linear"],["elevation"],-8000,"rgba(10,22,42,0.6)",-3000,"rgba(12,26,46,0.55)",-1500,"rgba(14,32,52,0.42)",-400,"rgba(20,48,64,0.2)",-80,"rgba(20,48,64,0)",0,"rgba(0,0,0,0)"],
    shade:{"hillshade-method":"multidirectional","hillshade-illumination-direction":[315,270,0,225],"hillshade-illumination-altitude":[40,35,35,50],
      "hillshade-highlight-color":["rgba(240,236,222,0.1)","rgba(240,236,222,0.04)","rgba(240,236,222,0.04)","rgba(240,236,222,0.02)"],
      "hillshade-shadow-color":["rgba(18,24,14,0.78)","rgba(18,24,14,0.42)","rgba(18,24,14,0.42)","rgba(18,24,14,0.2)"],
      "hillshade-accent-color":"rgba(18,24,14,0.3)","hillshade-exaggeration":1,"hillshade-illumination-anchor":"map"},
    depth:{"hillshade-method":"standard","hillshade-illumination-direction":315,"hillshade-illumination-anchor":"map","hillshade-highlight-color":"rgba(240,236,222,0.04)",
      "hillshade-shadow-color":"rgba(12,18,10,0.55)","hillshade-accent-color":"rgba(12,18,10,0)","hillshade-exaggeration":0.6} };
  var HELL={ sheet:"#1E080B",
    ground:["interpolate",["linear"],["elevation"],-8000,"#110407",-5000,"#18060A",-3000,"#20070C",-1500,"#2A0A0F",-500,"#360C11",-120,"#481116",-20,"#57151A",-1,"#5F181D",
      0,"#131215",200,"#151215",600,"#1A1214",1200,"#1F1416",2000,"#241418",3000,"#2B151A",4200,"#33161C",5600,"#3B171E"],
    shade:{"hillshade-method":"multidirectional","hillshade-illumination-direction":[315,270,0,225],"hillshade-illumination-altitude":[40,35,35,50],
      "hillshade-highlight-color":["rgba(150,164,186,0.2)","rgba(150,164,186,0.08)","rgba(150,164,186,0.08)","rgba(150,164,186,0.04)"],
      "hillshade-shadow-color":["rgba(0,0,0,0.8)","rgba(0,0,0,0.45)","rgba(0,0,0,0.45)","rgba(0,0,0,0.25)"],
      "hillshade-accent-color":"rgba(0,0,0,0.3)","hillshade-exaggeration":1,"hillshade-illumination-anchor":"map"},
    coast:"#521419",lake:"#3A0C11",lakeEdge:"#5E171C",river:"#9C252B",riverGlow:"#6A1318",grave:"#561519",graveEdge:"#74202A",
    town:"#1C1719",townWork:"#221C1E",road:["#2B1C1E","#3A2124","#4C2529"],rail:"#3A3034",building:"#201B1D",border:"rgba(170,58,62,0.32)" };
  var HELL_FONT={regular:["EBGaramond-Regular"],bold:["EBGaramond-SemiBold"],italic:["EBGaramond-Italic"]};
  var HELL_NAME={country:"#A9504C",state:"#8C4A47",city:"#CDBDB4",town:"#B4A39B",minor:"#9A8B85",water:"#B0605F",peak:"#958680",halo:"rgba(8,4,5,0.85)",haloWater:"rgba(24,6,9,0.8)"};
  var rgba=function(hex,a){ var n=parseInt(hex.slice(1),16); return "rgba("+(n>>16&255)+","+(n>>8&255)+","+(n&255)+","+a+")"; };
  var SKY_DAY={"atmosphere-blend":["interpolate",["linear"],["zoom"],0,1,4,0.8,7,0],"sky-color":"#1B242B","horizon-color":"#46545B","fog-color":"#46545B","sky-horizon-blend":0.6,"horizon-fog-blend":0.6,"fog-ground-blend":0.7};
  var SKY_HELL={"sky-color":"#0A0305","horizon-color":"#3A0C11","fog-color":"#1E080B","sky-horizon-blend":0.6,"horizon-fog-blend":0.5,"fog-ground-blend":0.8,"atmosphere-blend":["interpolate",["linear"],["zoom"],0,0.5,4,0.3,7,0]};

  /* ---------- the layers of each basemap ---------- */
  var kind=function(list){ return ["match",["get","class"],list,true,false]; };
  var fadeZ=function(z0,z1,a){ return ["interpolate",["linear"],["zoom"],z0,0,z1,a]; };
  function outlineLayers(){ var fade=function(a){ return fadeZ(3.5,6,a); }, road=function(w){ return ["interpolate",["exponential",1.4],["zoom"],5,w*.3,10,w,16,w*6]; };
    return [
      {id:"outline-ocean",type:"fill",source:"world-sheet",paint:{"fill-color":"#141C1F","fill-antialias":false}},
      {id:"outline-land",type:"fill",source:"countries",paint:{"fill-color":"#202825"}},
      {id:"outline-relief",type:"hillshade",source:"outline-dem",minzoom:3.5,paint:{"hillshade-exaggeration":.45,"hillshade-shadow-color":"#050504","hillshade-highlight-color":"#4A4A40","hillshade-accent-color":"#15150F"}},
      {id:"outline-water",type:"fill",source:"osm","source-layer":"water",minzoom:3.5,paint:{"fill-color":"#0B1017","fill-opacity":1}},
      {id:"outline-green",type:"fill",source:"osm","source-layer":"landcover",minzoom:5,filter:kind(["wood","forest","grass","wetland","farmland"]),
        paint:{"fill-color":["match",["get","class"],["wood","forest"],"#1C2A20","wetland","#1B2624","#212720"],"fill-opacity":fade(.8)}},
      {id:"outline-town",type:"fill",source:"osm","source-layer":"landuse",minzoom:6,filter:kind(["residential","commercial","industrial","retail","suburb","neighbourhood"]),
        paint:{"fill-color":["match",["get","class"],"industrial","#2A2826","#262625"],"fill-opacity":fade(.9)}},
      {id:"outline-waterway",type:"line",source:"osm","source-layer":"waterway",minzoom:6,paint:{"line-color":"#22323C","line-width":road(.9)}},
      {id:"outline-rail",type:"line",source:"osm","source-layer":"transportation",minzoom:9,filter:kind(["rail","transit"]),paint:{"line-color":"#46494A","line-width":1,"line-dasharray":[3,2]}},
      {id:"outline-road-minor",type:"line",source:"osm","source-layer":"transportation",minzoom:11,filter:kind(["minor","service","track","street","street_limited"]),paint:{"line-color":"#34373A","line-width":road(.45)}},
      {id:"outline-road",type:"line",source:"osm","source-layer":"transportation",minzoom:7,filter:kind(["secondary","tertiary"]),paint:{"line-color":"#44484A","line-width":road(.6)}},
      {id:"outline-road-major",type:"line",source:"osm","source-layer":"transportation",minzoom:4,filter:kind(["motorway","trunk","primary"]),paint:{"line-color":"#5E6264","line-width":road(.8),"line-opacity":fade(1)}},
      {id:"outline-buildings",type:"fill-extrusion",source:"osm","source-layer":"building",minzoom:13,paint:{"fill-extrusion-color":"#34383A","fill-extrusion-height":["coalesce",["get","render_height"],6],"fill-extrusion-base":["coalesce",["get","render_min_height"],0],"fill-extrusion-opacity":["interpolate",["linear"],["zoom"],13,0,14,.9]}},
      {id:"outline-line",type:"line",source:"countries",paint:{"line-color":"rgba(214,211,200,.17)","line-width":["interpolate",["linear"],["zoom"],3,.6,4,.9]}} ]; }
  function hellLayers(){ var road=function(w){ return ["interpolate",["exponential",1.4],["zoom"],4,w*.25,10,w,16,w*6]; };
    return [
      {id:"hell-sheet",type:"fill",source:"world-sheet",paint:{"fill-color":HELL.sheet,"fill-antialias":false}},
      {id:"hell-ground",type:"color-relief",source:"sea-dem",paint:{"color-relief-color":HELL.ground,"color-relief-opacity":1}},
      {id:"hell-shade",type:"hillshade",source:"outline-dem",paint:HELL.shade},
      {id:"hell-coast",type:"fill",source:"osm","source-layer":"water",minzoom:7,filter:["==",["get","class"],"ocean"],paint:{"fill-color":HELL.coast,"fill-opacity":fadeZ(7,9,1)}},
      {id:"hell-lake",type:"fill",source:"osm","source-layer":"water",filter:["!=",["get","class"],"ocean"],paint:{"fill-color":HELL.lake,"fill-outline-color":HELL.lakeEdge}},
      {id:"hell-town",type:"fill",source:"osm","source-layer":"landuse",minzoom:6,filter:kind(["residential","commercial","industrial","retail","suburb","neighbourhood"]),paint:{"fill-color":["match",["get","class"],"industrial",HELL.townWork,HELL.town],"fill-opacity":fadeZ(6,8,.9)}},
      {id:"hell-grave",type:"fill",source:"osm","source-layer":"landuse",minzoom:9,filter:["==",["get","class"],"cemetery"],paint:{"fill-color":HELL.grave,"fill-outline-color":HELL.graveEdge,"fill-opacity":fadeZ(9,11,.8)}},
      {id:"hell-river-glow",type:"line",source:"osm","source-layer":"waterway",minzoom:3,filter:["==",["get","class"],"river"],layout:{"line-cap":"round","line-join":"round"},paint:{"line-color":HELL.riverGlow,"line-width":road(4),"line-blur":road(3),"line-opacity":.45}},
      {id:"hell-river",type:"line",source:"osm","source-layer":"waterway",minzoom:3,layout:{"line-cap":"round","line-join":"round"},
        paint:{"line-color":HELL.river,"line-width":["interpolate",["exponential",1.4],["zoom"],4,["match",["get","class"],"river",.25,.11],10,["match",["get","class"],"river",1,.45],16,["match",["get","class"],"river",6,2.7]],
          "line-opacity":["interpolate",["linear"],["zoom"],8,["match",["get","class"],"river",.9,0],11,["match",["get","class"],"river",.9,.7]]}},
      {id:"hell-rail",type:"line",source:"osm","source-layer":"transportation",minzoom:9,filter:kind(["rail","transit"]),paint:{"line-color":HELL.rail,"line-width":1,"line-dasharray":[3,2]}},
      {id:"hell-road-minor",type:"line",source:"osm","source-layer":"transportation",minzoom:11,filter:kind(["minor","service","track","street","street_limited"]),paint:{"line-color":HELL.road[0],"line-width":road(.45)}},
      {id:"hell-road",type:"line",source:"osm","source-layer":"transportation",minzoom:7,filter:kind(["secondary","tertiary"]),paint:{"line-color":HELL.road[1],"line-width":road(.6)}},
      {id:"hell-road-major",type:"line",source:"osm","source-layer":"transportation",minzoom:4,filter:kind(["motorway","trunk","primary"]),paint:{"line-color":HELL.road[2],"line-width":road(.8),"line-opacity":fadeZ(4,6,1)}},
      {id:"hell-buildings",type:"fill-extrusion",source:"osm","source-layer":"building",minzoom:13,paint:{"fill-extrusion-color":HELL.building,"fill-extrusion-height":["coalesce",["get","render_height"],6],"fill-extrusion-base":["coalesce",["get","render_min_height"],0],"fill-extrusion-opacity":["interpolate",["linear"],["zoom"],13,0,14,.9]}},
      {id:"hell-border",type:"line",source:"countries",paint:{"line-color":HELL.border,"line-width":["interpolate",["linear"],["zoom"],2,.5,5,.9]}} ]; }
  function hellNameLayers(){ var nm=["coalesce",["get","name_en"],["get","name:latin"],["get","name"]];
    var cls=function(list){ return ["match",["get","class"],list,true,false]; };
    var zs=function(){ return ["interpolate",["linear"],["zoom"]].concat(Array.prototype.slice.call(arguments)); };
    var halo=function(c,w){ return {"text-halo-color":c,"text-halo-width":w,"text-halo-blur":0.6}; };
    return [
      {id:"hell-name-ocean",type:"symbol",source:"osm","source-layer":"water_name",filter:cls(["ocean","sea"]),layout:{"text-field":nm,"text-font":HELL_FONT.italic,"text-size":zs(1,11,6,16),"text-letter-spacing":0.22,"text-max-width":6},paint:Object.assign({"text-color":HELL_NAME.water},halo(HELL_NAME.haloWater,1))},
      {id:"hell-name-water",type:"symbol",source:"osm","source-layer":"water_name",minzoom:5,filter:["!",cls(["ocean","sea"])],layout:{"text-field":nm,"text-font":HELL_FONT.italic,"text-size":zs(5,11,14,14),"text-letter-spacing":0.08,"text-max-width":7},paint:Object.assign({"text-color":HELL_NAME.water},halo(HELL_NAME.haloWater,1))},
      {id:"hell-name-river",type:"symbol",source:"osm","source-layer":"waterway",minzoom:9,layout:{"text-field":nm,"text-font":HELL_FONT.italic,"text-size":zs(9,11,15,14),"symbol-placement":"line","text-letter-spacing":0.1},paint:Object.assign({"text-color":HELL_NAME.water},halo(HELL_NAME.haloWater,1))},
      {id:"hell-name-road",type:"symbol",source:"osm","source-layer":"transportation_name",minzoom:13,layout:{"text-field":nm,"text-font":HELL_FONT.regular,"text-size":zs(13,11,17,14),"symbol-placement":"line"},paint:Object.assign({"text-color":HELL_NAME.minor},halo(HELL_NAME.halo,1.2))},
      {id:"hell-name-peak",type:"symbol",source:"osm","source-layer":"mountain_peak",minzoom:9,layout:{"text-field":nm,"text-font":HELL_FONT.italic,"text-size":12,"text-max-width":7},paint:Object.assign({"text-color":HELL_NAME.peak},halo(HELL_NAME.halo,1.1))},
      {id:"hell-name-village",type:"symbol",source:"osm","source-layer":"place",minzoom:11,filter:cls(["village","hamlet","suburb","neighbourhood","quarter"]),layout:{"text-field":nm,"text-font":HELL_FONT.regular,"text-size":zs(11,11,16,14),"text-max-width":7},paint:Object.assign({"text-color":HELL_NAME.minor},halo(HELL_NAME.halo,1.2))},
      {id:"hell-name-town",type:"symbol",source:"osm","source-layer":"place",minzoom:7,filter:cls(["town"]),layout:{"text-field":nm,"text-font":HELL_FONT.regular,"text-size":zs(7,11,14,16),"text-max-width":7},paint:Object.assign({"text-color":HELL_NAME.town},halo(HELL_NAME.halo,1.2))},
      {id:"hell-name-state",type:"symbol",source:"osm","source-layer":"place",minzoom:4,maxzoom:9,filter:cls(["state","province"]),layout:{"text-field":nm,"text-font":HELL_FONT.italic,"text-size":zs(4,10,8,13),"text-transform":"uppercase","text-letter-spacing":0.15,"text-max-width":8},paint:Object.assign({"text-color":HELL_NAME.state,"text-opacity":0.9},halo(HELL_NAME.halo,1))},
      {id:"hell-name-city",type:"symbol",source:"osm","source-layer":"place",minzoom:3,filter:cls(["city"]),layout:{"text-field":nm,"text-font":HELL_FONT.bold,"text-size":zs(3,11,8,15,14,20),"text-max-width":7},paint:Object.assign({"text-color":HELL_NAME.city},halo(HELL_NAME.halo,1.3))},
      {id:"hell-name-country",type:"symbol",source:"osm","source-layer":"place",maxzoom:8,filter:cls(["country"]),layout:{"text-field":nm,"text-font":HELL_FONT.bold,"text-size":zs(1,10,3,13,6,17),"text-transform":"uppercase","text-letter-spacing":0.26,"text-max-width":7},paint:Object.assign({"text-color":HELL_NAME.country},halo(HELL_NAME.halo,1.3))} ]; }
  function nightLayers(){ var road=function(w){ return ["interpolate",["exponential",1.4],["zoom"],6,w*.3,10,w,16,w*5]; };
    return [
      {id:"night-sheet",type:"fill",source:"world-sheet",paint:{"fill-color":NIGHT.sheet,"fill-antialias":false}},
      {id:"night-lights",type:"raster",source:"night-lights",paint:{"raster-fade-duration":200,"raster-resampling":"linear"}},
      {id:"night-shade",type:"hillshade",source:"outline-dem",paint:NIGHT.shade},
      {id:"night-sea-glow",type:"color-relief",source:"sea-dem",paint:{"color-relief-color":NIGHT.seaGlow,"color-relief-opacity":1}},
      {id:"night-road-glow",type:"line",source:"osm","source-layer":"transportation",minzoom:7,filter:kind(["motorway","trunk","primary"]),layout:{"line-cap":"round","line-join":"round"},paint:{"line-color":NIGHT.roadGlow,"line-width":road(3),"line-blur":road(2.5),"line-opacity":fadeZ(7,10,.35)}},
      {id:"night-road-minor",type:"line",source:"osm","source-layer":"transportation",minzoom:11,filter:kind(["minor","service","street","street_limited"]),paint:{"line-color":NIGHT.road[0],"line-width":road(.4),"line-opacity":fadeZ(11,13,1)}},
      {id:"night-road",type:"line",source:"osm","source-layer":"transportation",minzoom:9,filter:kind(["secondary","tertiary"]),paint:{"line-color":NIGHT.road[1],"line-width":road(.5),"line-opacity":fadeZ(9,11,1)}},
      {id:"night-road-major",type:"line",source:"osm","source-layer":"transportation",minzoom:7,filter:kind(["motorway","trunk","primary"]),layout:{"line-cap":"round","line-join":"round"},paint:{"line-color":NIGHT.road[2],"line-width":road(.6),"line-opacity":fadeZ(7,9,1)}},
      {id:"night-border",type:"line",source:"countries",paint:{"line-color":NIGHT.border,"line-width":["interpolate",["linear"],["zoom"],2,.4,6,.8]}} ]; }
  /* ---------- one style, used by the globe and by the flat map's basemaps ---------- */
  var PLATE_URL=(typeof PLATE_IMG==="string"&&PLATE_IMG)?PLATE_IMG:"https://welcometoyourgalaxy.github.io/culprits/atlas-plate.webp";
  function baseStyle(projection){
    return { version:8, projection:{type:projection}, sky:SKY_DAY,
      glyphs:"https://welcometoyourgalaxy.github.io/culprits/glyphs/{fontstack}/{range}.pbf",
      sources:{
        base:{type:"raster",tiles:["https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{z}/{y}/{x}"],tileSize:256,maxzoom:18,attribution:"Imagery © Esri, Maxar"},
        hillshade:{type:"raster",tiles:["https://services.arcgisonline.com/arcgis/rest/services/Elevation/World_Hillshade/MapServer/tile/{z}/{y}/{x}"],tileSize:256,maxzoom:16,attribution:"Hillshade © Esri"},
        labels:{type:"raster",tiles:["https://a.basemaps.cartocdn.com/rastertiles/voyager_only_labels/{z}/{x}/{y}@2x.png?key=cb1_494p_1_eebbbfcb65bc573e54783d42"],tileSize:256,attribution:"Labels © CARTO, © OpenStreetMap"},
        "night-lights":{type:"raster",tiles:["gmonight://{z}/{y}/{x}"],tileSize:256,maxzoom:8,attribution:'<a href="https://earthobservatory.nasa.gov/features/NightLights" target="_blank" rel="noopener">NASA Black Marble 2016</a> via GIBS'},
        osm:OSM_SOURCE, "outline-dem":RELIEF_SOURCE, "sea-dem":TERRAIN_SOURCE, "world-sheet":WORLD_SHEET,
        countries:{type:"geojson",data:{type:"FeatureCollection",features:[]}}
      },
      layers:[
        {id:"bg",type:"background",paint:{"background-color":"#0B1017"}},
        {id:"base",type:"raster",source:"base",paint:Object.assign({"raster-opacity":1},BASE_GRADE.atlas)},
        {id:"hillshade",type:"raster",source:"hillshade",paint:{"raster-opacity":["interpolate",["linear"],["zoom"],PLATE.fadeIn,0,PLATE.fadeOut,.2,9,.34,13,.46]}}
      ] };
  }
  // Country shapes for the basemaps that draw land and borders themselves
  // (Standard, Hell, Bioluminescent): the flat map's own world-atlas file.
  function feedCountries(m){
    var c=window.__gmoCountries; if(!m) return;
    if(!c){ setTimeout(function(){ feedCountries(m); },400); return; }
    var s=m.getSource&&m.getSource("countries"); if(s) s.setData(c);
  }
  var hide=function(l){ l.layout=Object.assign({},l.layout||{},{visibility:"none"}); return l; };
  // Adds every basemap's layers to a map, hidden, and returns which layers
  // belong to which basemap. withAtlas: the globe's own painted atlas (the
  // flat map keeps the Leaflet atlas it always had).
  function addBasemaps(m, withAtlas, tag){
    var by={}, add=function(list,key){ var ids=[]; list.forEach(function(l){ try{ m.addLayer(hide(l)); ids.push(l.id); }catch(e){ console.warn("[globe] "+tag+" "+key+" layer "+l.id+":",e.message||e); } }); return ids; };
    by.jurassic=["base"].concat(add([
      {id:"sat-relief-colour",type:"color-relief",source:"outline-dem",paint:{"color-relief-color":SAT_RELIEF.colour,"color-relief-opacity":1}},
      {id:"sat-relief-seabed",type:"color-relief",source:"sea-dem",paint:{"color-relief-color":SAT_RELIEF.seabed,"color-relief-opacity":1}},
      {id:"sat-relief-shade",type:"hillshade",source:"outline-dem",paint:SAT_RELIEF.shade},
      {id:"sat-relief-depth",type:"hillshade",source:"outline-dem",paint:SAT_RELIEF.depth},
      {id:"sat-relief-sea",type:"color-relief",source:"sea-dem",paint:{"color-relief-color":SAT_RELIEF.sea,"color-relief-opacity":1}}],"jurassic"));
    if(withAtlas){
      // The washes and the plate sit UNDER the hillshade: drawn above it, the
      // plate kept showing at full strength after zooming in.
      try{ m.addLayer(atlasWashes,"hillshade"); }catch(e){ console.warn("[globe] atlas washes:",e.message||e); }
      m.addSource("plate-base",{type:"image",url:PLATE_URL,coordinates:[[-180,PLATE.top],[180,PLATE.top],[180,PLATE.bot],[-180,PLATE.bot]]});
      m.addLayer({id:"plate-base",type:"raster",source:"plate-base",paint:{"raster-opacity":["interpolate",["linear"],["zoom"],PLATE.fadeIn,1,PLATE.fadeOut,0],"raster-fade-duration":0}},"hillshade");
      by.atlas=["base","hillshade","plate-base"];
    }
    by.outlines=add(outlineLayers(),"standard");
    by.hell=add(hellLayers(),"hell").concat(add(hellNameLayers(),"hell names"));
    by.night=add(nightLayers(),"night");
    feedCountries(m);
    m.addLayer({id:"labels",type:"raster",source:"labels",paint:{"raster-opacity":.92}});
    return by;
  }
  // Shows one basemap's layers on a map and hides the rest.
  function showBasemap(m, by, kind, isGlobe){
    if(!m||!by||!m.getLayer("labels")) return;
    var vis=function(id,on){ if(m.getLayer(id)) m.setLayoutProperty(id,"visibility",on?"visible":"none"); };
    var all={}; Object.keys(by).forEach(function(k){ by[k].forEach(function(id){ all[id]=1; }); });
    Object.keys(all).forEach(function(id){ vis(id,false); });
    (by[kind]||[]).forEach(function(id){ vis(id,true); });
    if(kind==="atlas"||kind==="jurassic"){ Object.keys(BASE_GRADE[kind]).forEach(function(k){ m.setPaintProperty("base",k,BASE_GRADE[kind][k]); }); }
    vis("labels",kind!=="hell");
    m.setPaintProperty("labels","raster-opacity",kind==="atlas"?["interpolate",["linear"],["zoom"],PLATE.fadeIn,0,PLATE.fadeOut,.92]:kind==="jurassic"?.8:.92);
    m.setPaintProperty("labels","raster-saturation",kind==="atlas"||kind==="hell"?0:-1);
    m.setPaintProperty("labels","raster-brightness-min",kind==="night"||kind==="outlines"?0.8:0);
    m.setPaintProperty("labels","raster-brightness-max",kind==="night"||kind==="outlines"?0.1:1);
    if(isGlobe){ try{ m.setSky(kind==="night"?NIGHT.sky:kind==="hell"?SKY_HELL:SKY_DAY); }catch(e){} }
    m.triggerRepaint();
  }

  /* ---------- the globe ---------- */
  var OPENING_ZOOM=1.35;
  var globe=new maplibregl.Map({
    container:"globeMap", renderWorldCopies:false, fadeDuration:0, maxPitch:85, rollEnabled:true,
    pixelRatio:Math.min(window.devicePixelRatio||1,1.5),
    center:[12,24], zoom:OPENING_ZOOM, minZoom:0.4,
    attributionControl:{compact:true}, style:baseStyle("vertical-perspective")
  });
  window.gmoGlobe=globe;
  var GLOBE_BY=null;
  // The planet sits in the room the side columns leave, not under them.
  function fitPadding(){
    try{ var w=window.innerWidth, h=window.innerHeight, sb=document.getElementById("sidebar"), rb=document.getElementById("rightbar"), ip=document.getElementById("infoPanel");
      var left=0, right=0; [sb,ip].forEach(function(el){ if(el&&el.offsetWidth){ var r=el.getBoundingClientRect(); if(r.left<w/2) left=Math.max(left,r.right); } });
      if(rb&&rb.offsetWidth){ var rr=rb.getBoundingClientRect(); right=Math.max(0,w-rr.left); }
      if(w<900){ left=0; right=0; }
      globe.setPadding({left:Math.min(left,w*0.45),right:Math.min(right,w*0.3),top:70,bottom:20}); }catch(e){}
  }
  window.addEventListener("resize",fitPadding);

  globe.on("load",function(){
    GLOBE_BY=addBasemaps(globe,true,"globe");
    // What the flat map draws, copied (see the mirror below).
    globe.addSource("mirror",{type:"geojson",data:{type:"FeatureCollection",features:[]},promoteId:"fid"});
    globe.addLayer({id:"mirror-fill",type:"fill",source:"mirror",filter:["all",["==",["get","g"],"area"],["get","fill"]],
      paint:{"fill-color":["get","fc"],"fill-opacity":["get","fo"],"fill-antialias":false}});
    globe.addLayer({id:"mirror-line",type:"line",source:"mirror",filter:["all",["!=",["get","g"],"point"],["get","stroke"],["!",["get","dash"]]],
      layout:{"line-join":"round","line-cap":"round"},paint:{"line-color":["get","c"],"line-opacity":["get","o"],"line-width":["get","w"]}});
    globe.addLayer({id:"mirror-dash",type:"line",source:"mirror",filter:["all",["!=",["get","g"],"point"],["get","stroke"],["get","dash"]],
      paint:{"line-color":["get","c"],"line-opacity":["get","o"],"line-width":["get","w"],"line-dasharray":[2,1.6]}});
    globe.addLayer({id:"mirror-hover",type:"line",source:"mirror",filter:["==",["get","g"],"area"],
      paint:{"line-color":"rgba(223,231,245,0.75)","line-width":1.6,"line-opacity":["case",["boolean",["feature-state","hover"],false],1,0]}});
    globe.addLayer({id:"mirror-pt",type:"circle",source:"mirror",filter:["==",["get","g"],"point"],
      paint:{"circle-radius":["get","r"],"circle-color":["get","fc"],"circle-opacity":["get","fo"],
        "circle-stroke-color":["get","c"],"circle-stroke-width":["case",["get","stroke"],["get","w"],0],"circle-stroke-opacity":["get","o"]}});
    // The markers: the same points, colours and sizes the flat map draws.
    globe.addSource("points",{type:"geojson",data:{type:"FeatureCollection",features:[]}});
    var imp=["match",["get","i"],5,1.7,4,1.45,3,1.25,2,1.08,1];
    var rad=function(k){ var e=["interpolate",["linear"],["zoom"]]; [[0,1.5],[3,2.2],[5,3.2],[7,4.4],[9,5.6],[12,7]].forEach(function(s){ e.push(s[0],["*",s[1]*k,imp]); }); return e; };
    globe.addLayer({id:"pt-glow",type:"circle",source:"points",paint:{"circle-color":["get","c"],"circle-opacity":0.28,"circle-blur":1,"circle-radius":rad(2.4)}});
    globe.addLayer({id:"pt-core",type:"circle",source:"points",paint:{"circle-color":["get","c"],"circle-opacity":0.95,"circle-radius":rad(1),"circle-stroke-color":"rgba(8,12,27,0.85)","circle-stroke-width":0.8}});
    // Hell's own names go over everything but the markers.
    (GLOBE_BY.hell||[]).forEach(function(id){ if(/^hell-name-/.test(id)) try{ globe.moveLayer(id,"mirror-hover"); }catch(e){} });
    showBasemap(globe,GLOBE_BY,BASEMAP,true);
    fitPadding(); globe.jumpTo({center:[12,24],zoom:OPENING_ZOOM});
    feedPoints(); syncMirror(true);
  });

  /* ---------- the flat map's basemaps ---------- */
  // Atlas is the Leaflet atlas the flat map has always drawn. The others are
  // MapLibre drawn inside Leaflet as one layer, in their own pane under the
  // country shapes and markers; while one of them shows, the atlas's panes
  // are hidden.
  var ATLAS_PANES=["tilePane","satSea","satWash","satWarm","satShade","satLabels","plate"];
  var flatGL=null, FLAT_BY=null, VIEW="globe";
  function freeConstrain(lngLat,zoom){ return {center:new maplibregl.LngLat(Math.max(-540,Math.min(540,lngLat.lng)),Math.max(-89.9,Math.min(89.9,lngLat.lat))),zoom:zoom==null?0:zoom}; }
  function flatMap(){ return (typeof map!=="undefined"&&map&&typeof map.setView==="function")?map:null; }
  function ensureFlatGL(){
    var m=flatMap(); if(flatGL||!m||!L.maplibreGL) return;
    if(!m.getPane("glBase")){ m.createPane("glBase"); m.getPane("glBase").style.zIndex=205; m.getPane("glBase").style.pointerEvents="none"; }
    flatGL=L.maplibreGL({style:baseStyle("mercator"),pane:"glBase",interactive:false,renderWorldCopies:false,fadeDuration:0,
      transformConstrain:freeConstrain,pixelRatio:Math.min(window.devicePixelRatio||1,1.5)}).addTo(m);
    var gm=flatGL.getMaplibreMap();
    gm.on("load",function(){ FLAT_BY=addBasemaps(gm,false,"flat"); showBasemap(gm,FLAT_BY,BASEMAP,false); });
  }
  function flatBasemap(kind){
    var m=flatMap(); if(!m) return;
    var atlas=(kind==="atlas");
    ATLAS_PANES.forEach(function(p){ var el=m.getPane(p); if(el) el.style.display=atlas?"":"none"; });
    if(!atlas) ensureFlatGL();
    var gp=m.getPane("glBase"); if(gp) gp.style.display=atlas?"none":"";
    if(!atlas&&flatGL&&FLAT_BY) showBasemap(flatGL.getMaplibreMap(),FLAT_BY,kind,false);
  }

  /* ---------- basemaps on and off, in both views ---------- */
  function setBasemap(kind){
    if(!BASEMAPS.some(function(b){ return b[0]===kind; })) kind="atlas";
    BASEMAP=kind; try{ localStorage.setItem(BM_KEY,kind); }catch(e){}
    Array.prototype.forEach.call(ctl.querySelectorAll("button.bm"),function(b){ b.classList.toggle("on",b.dataset.bm===kind); });
    // Only the map in view loads the new basemap; the other catches up when
    // it is switched to, so the two are never loading tiles at once.
    if(VIEW==="globe") showBasemap(globe,GLOBE_BY,kind,true); else flatBasemap(kind);
  }

  /* ---------- the record markers, fed from the flat map's own filtered set ---------- */
  function feedPoints(){
    var pts=window.__pjPts||[], src=globe.getSource("points"); if(!src) return;
    var feats=[];
    for(var i=0;i<pts.length;i++){ var o=pts[i]; if(typeof o.la!=="number"||typeof o.lo!=="number") continue;
      feats.push({type:"Feature",properties:{k:i,c:o.c||"#9aa4c7",i:o.i||1,n:(o.p&&(o.p.name||o.p.title))||""},geometry:{type:"Point",coordinates:[o.lo,o.la]}}); }
    src.setData({type:"FeatureCollection",features:feats});
  }
  window.addEventListener("pj:rebuilt",feedPoints);

  /* ---------- the mirror: everything else the flat map draws ---------- */
  // Every shape and marker on the flat map (country outlines and highlights,
  // regime outlines, shaded areas, drilled regions, international bodies) is
  // copied with its own colour, line and fill, in the flat map's drawing
  // order. Filters and highlights change the flat map; the copy follows.
  var MIRROR_LAYERS=[], geomCache={}, mirrorDirty=true, mirrorTimer=null;
  function paneZ(name){ var m=flatMap(); var el=m&&m.getPane(name||"overlayPane"); var z=el&&parseInt(el.style.zIndex||getComputedStyle(el).zIndex,10); return isNaN(z)?400:z; }
  function iconColours(l){
    var html=(l.options.icon&&l.options.icon.options&&l.options.icon.options.html)||"", sz=(l.options.icon&&l.options.icon.options&&l.options.icon.options.iconSize)||[14,14];
    var bg=/background(?:-color)?\s*:\s*(#[0-9a-fA-F]{3,8}|rgba?\([^)]*\))/.exec(html), bd=/border\s*:\s*[\d.]+px\s+\w+\s+(#[0-9a-fA-F]{3,8}|rgba?\([^)]*\))/.exec(html);
    return {fc:bg?bg[1]:"#9aa4c7", c:bd?bd[1]:"rgba(8,12,27,0.85)", r:Math.max(4,(Array.isArray(sz)?sz[0]:14)/2)};
  }
  function syncMirror(force){
    var src=globe.getSource&&globe.getSource("mirror"), m=flatMap(); if(!src||!m) return;
    if(!force&&!mirrorDirty) return; mirrorDirty=false;
    var list=[];
    m.eachLayer(function(l){
      if(l instanceof L.Path || (l instanceof L.Marker && l.options && l.options.icon)) list.push(l);
    });
    list.sort(function(a,b){ var za=paneZ(a.options.pane||(a instanceof L.Marker?"markerPane":"overlayPane")), zb=paneZ(b.options.pane||(b instanceof L.Marker?"markerPane":"overlayPane")); return za-zb || L.stamp(a)-L.stamp(b); });
    var feats=[]; MIRROR_LAYERS=[];
    list.forEach(function(l){
      var id=L.stamp(l), o=l.options||{}, geom=null, g;
      if(l instanceof L.Marker){ var ll=l.getLatLng(); geom={type:"Point",coordinates:[ll.lng,ll.lat]}; g="point"; }
      else {
        var key=l._latlngs||l._latlng, c=geomCache[id];
        if(c&&c.key===key) geom=c.geom; else { try{ geom=l.toGeoJSON().geometry; }catch(e){ geom=null; } geomCache[id]={key:key,geom:geom}; }
        if(!geom) return;
        g=(l instanceof L.CircleMarker)?"point":(l instanceof L.Polygon)?"area":"line";
      }
      var p=(l.feature&&l.feature.properties)||{};
      var props={fid:MIRROR_LAYERS.length, g:g, n:String(p.name||p.NAME||p.title||p.shapeName||""),
        stroke:o.stroke!==false, c:o.color||"#3388ff", o:(o.opacity==null?1:o.opacity), w:(o.weight==null?3:o.weight),
        fill:(g==="area"||g==="point")?(o.fill!==false):false, fc:o.fillColor||o.color||"#3388ff", fo:(o.fillOpacity==null?0.2:o.fillOpacity),
        dash:!!o.dashArray, r:(o.radius==null?6:o.radius), click:o.interactive!==false};
      if(l instanceof L.Marker){ var ic=iconColours(l); props.fc=ic.fc; props.c=ic.c; props.r=ic.r; props.w=2; props.fo=1; props.o=1; props.fill=true; props.stroke=true;
        props.n=String((l.options.title)||(l.getTooltip&&l.getTooltip()&&l.getTooltip().getContent&&typeof l.getTooltip().getContent()==="string"?l.getTooltip().getContent():"")||""); }
      MIRROR_LAYERS.push(l);
      feats.push({type:"Feature",properties:props,geometry:geom});
    });
    src.setData({type:"FeatureCollection",features:feats});
  }
  function markDirty(){ mirrorDirty=true; if(VIEW!=="globe") return; clearTimeout(mirrorTimer); mirrorTimer=setTimeout(function(){ syncMirror(false); },200); }
  (function hook(){
    var m=flatMap(); if(!m){ setTimeout(hook,300); return; }
    m.on("layeradd layerremove",markDirty);
    var ps=L.Path.prototype.setStyle; L.Path.prototype.setStyle=function(){ var r=ps.apply(this,arguments); if(this._map) markDirty(); return r; };
    var mi=L.Marker.prototype.setIcon; L.Marker.prototype.setIcon=function(){ var r=mi.apply(this,arguments); if(this._map) markDirty(); return r; };
  })();

  /* ---------- hovering, clicking, and dropping into the flat map ---------- */
  var tip=document.getElementById("globeTip"), hoverId=null;
  var esc=function(s){ return String(s).replace(/[<>&]/g,function(ch){ return {"<":"&lt;",">":"&gt;","&":"&amp;"}[ch]; }); };
  function setHover(id){ if(id===undefined||id===null||isNaN(id)) id=null; if(hoverId===id) return;
    if(hoverId!==null) try{ globe.setFeatureState({source:"mirror",id:hoverId},{hover:false}); }catch(e){}
    hoverId=id; if(hoverId!==null) try{ globe.setFeatureState({source:"mirror",id:hoverId},{hover:true}); }catch(e){} }
  function topMirror(point){
    var fs=globe.queryRenderedFeatures(point,{layers:["mirror-pt","mirror-fill","mirror-line","mirror-dash"]}).filter(function(f){ return f.properties.click; });
    if(!fs.length) return null;
    var pts=fs.filter(function(f){ return f.properties.g==="point"; }); if(pts.length) fs=pts;
    fs.sort(function(a,b){ return b.properties.fid-a.properties.fid; });
    return fs[0];
  }
  // A readable name for the spot: some layers store only a country code.
  function nameAt(point,top){
    if(top.properties.n&&!/^[A-Z]{2,3}$/.test(top.properties.n)) return top.properties.n;
    var fs=globe.queryRenderedFeatures(point,{layers:["mirror-fill","mirror-line","mirror-dash"]});
    for(var i=0;i<fs.length;i++){ var n=fs[i].properties.n; if(n&&!/^[A-Z]{2,3}$/.test(n)) return n; }
    return top.properties.n;
  }
  function showTip(e,html){ tip.innerHTML=html; tip.style.display="block"; tip.style.left=(e.point.x+14)+"px"; tip.style.top=(e.point.y+10)+"px"; }
  globe.on("mousemove",function(e){
    var pts=globe.queryRenderedFeatures(e.point,{layers:["pt-glow","pt-core"]});
    if(pts.length){ setHover(null); globe.getCanvas().style.cursor="pointer";
      var names=[]; for(var i=0;i<pts.length&&names.length<4;i++){ var n=pts[i].properties.n; if(n&&names.indexOf(n)<0) names.push(n); }
      showTip(e,"<b>"+names.map(esc).join("<br>")+(pts.length>names.length?"<br>&hellip; "+pts.length+" records here":"")+"</b><span>Click to open on the flat map</span>"); return; }
    var f=topMirror(e.point);
    if(f){ setHover(f.properties.g==="area"?f.properties.fid:null); globe.getCanvas().style.cursor="pointer";
      showTip(e,(nameAt(e.point,f)?"<b>"+esc(nameAt(e.point,f))+"</b>":"")+"<span>Click to open on the flat map</span>"); return; }
    setHover(null); globe.getCanvas().style.cursor=""; tip.style.display="none";
  });
  globe.on("mouseout",function(){ setHover(null); tip.style.display="none"; });
  var dragged=false; globe.on("dragstart",function(){ dragged=true; }); globe.on("dragend",function(){ setTimeout(function(){ dragged=false; },50); });
  globe.on("click",function(e){
    if(dragged) return;
    var pts=globe.queryRenderedFeatures(e.point,{layers:["pt-glow","pt-core"]});
    if(pts.length){ var o=(window.__pjPts||[])[pts[0].properties.k]; if(!o) return;
      toFlat([o.la,o.lo],Math.max(6,Math.round(globe.getZoom()+1)),function(){ if(typeof window.pjGlobeOpen==="function") window.pjGlobeOpen(o); }); return; }
    var f=topMirror(e.point); if(!f) return;
    var l=MIRROR_LAYERS[f.properties.fid]; if(!l) return;
    var ll=(l instanceof L.Marker)?l.getLatLng():L.latLng(e.lngLat.lat,e.lngLat.lng);
    toFlat([ll.lat,ll.lng],Math.max(3,Math.round(globe.getZoom()+1)),function(){
      try{ var m=flatMap(), cp=m.latLngToContainerPoint(ll);
        l.fire("click",{latlng:ll,layerPoint:m.latLngToLayerPoint(ll),containerPoint:cp,originalEvent:new MouseEvent("click",{clientX:cp.x,clientY:cp.y})}); }
      catch(err){ console.warn("[globe] open on flat map:",err.message||err); } });
  });

  /* ---------- the two views ---------- */
  var bGlobe=document.getElementById("gbViewGlobe"), bFlat=document.getElementById("gbViewFlat");
  function toFlat(center,zoom,after){
    var m=flatMap(); VIEW="flat";
    bGlobe.classList.remove("on"); bFlat.classList.add("on");
    if(!center&&m){ var c=globe.getCenter(); center=[c.lat,c.lng]; zoom=Math.max(2,Math.round(globe.getZoom()+1)); }
    document.body.classList.remove("globe-on"); box.classList.add("off"); tip.style.display="none";
    if(m){ try{ m.invalidateSize(false); }catch(e){} try{ if(center) m.setView(center,zoom,{animate:false}); }catch(e){} }
    flatBasemap(BASEMAP);
    if(after) setTimeout(after,80);
  }
  function toGlobe(){
    var m=flatMap(); VIEW="globe";
    bFlat.classList.remove("on"); bGlobe.classList.add("on");
    if(m){ try{ var c=m.getCenter(); globe.jumpTo({center:[c.lng,Math.max(-80,Math.min(80,c.lat))],zoom:Math.max(0.4,m.getZoom()-1),pitch:0,bearing:0}); }catch(e){} }
    document.body.classList.add("globe-on"); box.classList.remove("off");
    showBasemap(globe,GLOBE_BY,BASEMAP,true);
    syncMirror(false);
    setTimeout(function(){ try{ globe.resize(); }catch(e){} },30);
  }
  window.gmoToFlat=toFlat; window.gmoToGlobe=toGlobe;
  bGlobe.addEventListener("click",function(){ if(VIEW!=="globe") toGlobe(); });
  bFlat.addEventListener("click",function(){ if(VIEW!=="flat") toFlat(); });
  document.getElementById("gbBasemaps").addEventListener("click",function(e){ var b=e.target.closest&&e.target.closest("button.bm"); if(b) setBasemap(b.dataset.bm); });
  document.getElementById("gbZoomIn").addEventListener("click",function(){ var m=flatMap(); if(VIEW==="globe") globe.zoomIn(); else if(m) m.zoomIn(); });
  document.getElementById("gbZoomOut").addEventListener("click",function(){ var m=flatMap(); if(VIEW==="globe") globe.zoomOut(); else if(m) m.zoomOut(); });
  document.getElementById("gbWorld").addEventListener("click",function(){
    if(VIEW==="globe"){ fitPadding(); globe.easeTo({center:[globe.getCenter().lng,20],zoom:OPENING_ZOOM,pitch:0,bearing:0,roll:0,duration:900}); return; }
    var m=flatMap(); if(!m) return;
    try{ if(typeof deactivate==="function") deactivate(); }catch(e){}
    try{ m.closePopup(); m.setView([25,10],3); }catch(e){}
  });

  // The globe is the opening view.
  document.body.classList.add("globe-on");
})();
</script>
<!-- ====================================================== end of the globe -->
"""

P = pathlib.Path("index.html")
if not P.exists():
    sys.exit("index.html not found - run this from the GMO-map repo root")
s = P.read_text(encoding="utf-8")

if "the mirror: everything else the flat map draws" in s:
    print("already applied"); sys.exit(0)

START = "<!-- ======================================================================\n     THE GLOBE."
END = "<!-- ====================================================== end of the globe -->\n"
a, b = s.find(START), s.find(END)
if a < 0 or b < 0 or s.count(START) != 1 or s.count(END) != 1:
    sys.exit("the first globe block was not found once - run patch_globe.py first")
s = s[:a] + BLOCK + s[b + len(END):]

old = "map.setMaxBounds([[-85,-250],[85,250]]);"
if s.count(old) != 1:
    sys.exit("expected exactly one match for the flat map's edge limit")
s = s.replace(old, "/* No edge limit: the flat map drags freely past the edges of the world. */")

P.write_text(s, encoding="utf-8")
print("applied: basemaps on both views, free drag, the flat map's shapes on the globe, box top right, no hologram")
