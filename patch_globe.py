#!/usr/bin/env python3
"""The globe: the map opens as a planet with the Culprits basemaps (Jurassic,
Atlas, Bioluminescent, Hologram, Hell, Standard), carrying the flat map's own
markers; "Flat map" is the Leaflet map as it was.

Run from the repo root:  python3 patch_globe.py
Applies by exact-text match, refuses to run twice, exits 0 when already done.
Four one-line hooks go into the flat map's code (so the globe can read the
filtered markers, open a marker's popup, and open a country); everything else
is one block at the foot of the file, between two comment bars.
"""
import pathlib, sys

P = pathlib.Path("index.html")
if not P.exists():
    sys.exit("index.html not found - run this from the GMO-map repo root")
s = P.read_text(encoding="utf-8")

if 'id="globe-script"' in s:
    print("already applied"); sys.exit(0)

BLOCK = r"""<!-- ======================================================================
     THE GLOBE. The map opens as a planet (MapLibre, vertical-perspective
     projection) carrying the markers the flat map draws, with the basemaps
     from the Culprits atlas: Jurassic, Atlas, Bioluminescent, Hologram,
     Hell, Standard. "Flat map" is the Leaflet map this file has always
     been; it is untouched. Clicking a marker or a country on the globe
     drops into the flat map at that spot and opens what the flat map would
     open. Everything here lives between these two comment bars.
     ====================================================================== -->
<link rel="stylesheet" href="https://unpkg.com/maplibre-gl@5.24.0/dist/maplibre-gl.css">
<script src="https://unpkg.com/maplibre-gl@5.24.0/dist/maplibre-gl.js"></script>
<style id="globe-style">
  #globe{position:absolute;left:0;top:0;width:100%;height:100vh;z-index:900;background:#040611;
    transition:opacity .35s ease;}
  #globe.off{opacity:0;pointer-events:none;visibility:hidden;}
  #globe .maplibregl-canvas-container,#globe .maplibregl-canvas{outline:none;}
  #globeStars{position:absolute;inset:0;width:100%;height:100%;pointer-events:none;}
  #globeMap{position:absolute;inset:0;}
  body.globe-on #map{visibility:hidden;}
  /* Flat-map-only furniture that has no meaning on the globe. */
  body.globe-on #gbCrumb{display:none!important;}
  #globeTip{position:absolute;z-index:3;pointer-events:none;display:none;max-width:260px;padding:5px 9px;
    background:rgba(8,12,27,0.95);border:1px solid var(--accent-soft);border-radius:7px;color:#e3e6ef;
    font-size:11.5px;line-height:1.35;box-shadow:0 3px 14px rgba(0,0,0,.5);}
  #globeTip b{display:block;color:#f0ece4;font-weight:600;}
  #globeTip span{color:#969eb1;}
  /* The view box: at the foot of the screen, between the side columns. */
  #globeBox{position:fixed;left:50%;bottom:14px;transform:translateX(-50%);z-index:1003;display:flex;align-items:center;
    gap:10px;padding:7px 10px;background:rgba(8,12,27,0.95);border:1px solid var(--accent-soft);border-radius:10px;
    backdrop-filter:blur(10px);box-shadow:0 4px 22px rgba(0,0,0,0.45);font-family:'Marcellus','Georgia',serif;
    font-size:12px;color:#d6dae8;max-width:calc(100vw - 24px);flex-wrap:wrap;justify-content:center;}
  #globeBox .gb-grp{display:flex;align-items:center;gap:5px;}
  #globeBox .gb-cap{font-size:10px;letter-spacing:.6px;text-transform:uppercase;color:#8a93ad;margin-right:2px;}
  #globeBox button{font:inherit;font-size:12px;color:#d6dae8;background:rgba(20,27,56,0.55);border:1px solid var(--accent-soft);
    border-radius:7px;padding:5px 10px;cursor:pointer;line-height:1.2;white-space:nowrap;}
  #globeBox button:hover{background:rgba(34,46,98,0.75);color:#fff;}
  #globeBox button.on{background:#2e3e72;color:#fff;border-color:#4e62a8;}
  #globeBox .gb-zoom button{width:30px;padding:5px 0;font-size:15px;font-weight:700;}
  #globeBox .gb-sep{width:1px;height:22px;background:var(--accent-soft);}
  #globeBox .gb-sub{display:block;font-size:9.5px;color:#8a93ad;letter-spacing:.2px;margin-top:1px;}
  #globeBox button.bm{text-align:center;padding:4px 8px;}
  #globeBox button.bm.on .gb-sub{color:#c9d1ee;}
  @media (max-width:900px){ #globeBox{bottom:8px;gap:6px;padding:6px 8px;font-size:11px;} #globeBox button{padding:4px 7px;} }
  /* Hologram: the screen behind the planet, scan lines, a tube's rounded dark edge. */
  :root{--holo-bg:#081729;--holo-earth:#0f2440;--holo-line:#7fb8d9;--holo-glow:#5b9cc8;--holo-grid:rgba(127,184,217,0.15);
    --holo-detail:#6d9fc0;--holo-fringe:#6fb0bd;}
  .holo-scan,.holo-crt,.holo-rim{position:absolute;pointer-events:none;display:none;}
  #globe.holo-on .holo-scan,#globe.holo-on .holo-crt,#globe.holo-on .holo-rim{display:block;}
  #globe.holo-on{background:radial-gradient(ellipse at 50% 45%, #0e2037 0%, var(--holo-bg) 70%);}
  .holo-rim{left:0;top:0;width:100%;height:100%;z-index:2;}
  .holo-scan{inset:0;opacity:.04;z-index:2;background:repeating-linear-gradient(to bottom, var(--holo-line) 0 1px, transparent 1px 3px);}
  .holo-crt{inset:0;z-index:2;border-radius:18px;background:radial-gradient(ellipse at center, transparent 58%, rgba(2,4,14,.38) 100%);
    box-shadow:inset 0 0 70px rgba(2,4,14,.55);}
</style>
<script id="globe-script">
(function(){
  "use strict";
  if(typeof maplibregl==="undefined"||!maplibregl.Map){ console.warn("[globe] MapLibre did not load; the flat map stands alone."); return; }
  var mapEl=document.getElementById("map"); if(!mapEl) return;

  /* ---------- the page: a container after the flat map, and the view box ---------- */
  var box=document.createElement("div"); box.id="globe";
  box.innerHTML='<canvas id="globeStars"></canvas><div id="globeMap"></div>'+
    '<div class="holo-scan"></div><div class="holo-crt"></div><canvas class="holo-rim"></canvas><div id="globeTip"></div>';
  mapEl.parentNode.insertBefore(box, mapEl.nextSibling);

  // The basemaps as the Culprits atlas names them, with a word for a reader
  // who has never seen them. Woodlands is left out at the owner's word.
  var BASEMAPS=[
    ["jurassic","Jurassic","photograph, shaded relief","The satellite photograph of Earth with shaded relief laid over it in earth tones."],
    ["atlas","Atlas","painted chart","The painted world chart. Zoom in and it gives way to the photograph underneath."],
    ["night","Bioluminescent","Earth at night","NASA's picture of the planet's lights after dark, in navy and ice, with a glow along every shore."],
    ["holo","Hologram","glowing wireframe","Country outlines as a glowing wireframe on a dark screen, with streets drawn in close up."],
    ["hell","Hell","oxblood and basalt","The same Earth drawn in oxblood sea, black land and red rivers."],
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

  /* ---------- the painted plate, cut into map squares ---------- */
  // The same plate the flat map lays over its imagery (PLATE_IMG), registered
  // in Mercator between the same latitudes, fading out between zoom 3 and 5.
  var PLATE={ top:85.05112877980659, bot:-80.55, fadeIn:3, fadeOut:5 };
  var plateBitmap=null;
  var plateMerc=function(lat){ return (1-Math.log(Math.tan(Math.PI/4+lat*Math.PI/360))/Math.PI)/2; };
  function platePiece(z,x,y){
    if(!plateBitmap){
      var src=(typeof PLATE_IMG==="string"&&PLATE_IMG)?PLATE_IMG:"https://welcometoyourgalaxy.github.io/culprits/atlas-plate.webp";
      plateBitmap=fetch(src).then(function(r){ if(!r.ok) throw new Error(""+r.status); return r.blob(); }).then(function(b){ return createImageBitmap(b); });
      plateBitmap.catch(function(){ plateBitmap=null; });
    }
    return plateBitmap.then(function(img){
      var n=Math.pow(2,z), top=plateMerc(PLATE.top), bot=plateMerc(PLATE.bot);
      var cv=cv256(256,256), ctx=cv.getContext("2d");
      var y0=y/n, y1=(y+1)/n, a=Math.max(y0,top), b=Math.min(y1,bot);
      if(b>a){ var sy=(a-top)/(bot-top)*img.height, sh=(b-a)/(bot-top)*img.height;
        var dy=(a-y0)*n*256, dh=(b-a)*n*256;
        ctx.imageSmoothingQuality="high";
        ctx.drawImage(img, x/n*img.width, sy, img.width/n, sh, 0, dy, 256, dh); }
      return rawPng(ctx.getImageData(0,0,256,256).data,256,256); });
  }
  maplibregl.addProtocol("gmoplate", function(params){
    var m=params.url.match(/^gmoplate:\/\/(\d+)\/(\d+)\/(\d+)/); if(!m) return Promise.reject(new Error("not a plate square"));
    return platePiece(+m[1],+m[2],+m[3]).then(function(d){ return {data:d}; }); });

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
  var HOLO={ bg:"#081729",earth:"#0f2440",line:"#7fb8d9",glow:"#5b9cc8",grid:"rgba(127,184,217,0.15)",detail:"#6d9fc0",fringe:"#6fb0bd" };
  var rgba=function(hex,a){ var n=parseInt(hex.slice(1),16); return "rgba("+(n>>16&255)+","+(n>>8&255)+","+(n&255)+","+a+")"; };
  var SKY_DAY={"atmosphere-blend":["interpolate",["linear"],["zoom"],0,1,4,0.8,7,0],"sky-color":"#1B242B","horizon-color":"#46545B","fog-color":"#46545B","sky-horizon-blend":0.6,"horizon-fog-blend":0.6,"fog-ground-blend":0.7};
  var SKY_HOLO={"sky-color":HOLO.bg,"horizon-color":HOLO.bg,"fog-color":HOLO.bg,"atmosphere-blend":0,"sky-horizon-blend":0.5,"horizon-fog-blend":0.5,"fog-ground-blend":0.5};
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
  function holoLayers(){ var line={"line-join":"round","line-cap":"round"}, c=HOLO;
    var f=function(a){ return ["interpolate",["linear"],["zoom"],6,a,9,a*0.4]; };
    return [
      {id:"holo-earth",type:"background",paint:{"background-color":c.earth}},
      {id:"holo-grat",type:"line",source:"holo-graticule",layout:line,paint:{"line-color":c.grid,"line-width":0.8}},
      {id:"holo-relief",type:"hillshade",source:"outline-dem",minzoom:3,paint:{"hillshade-exaggeration":0.5,"hillshade-illumination-direction":315,"hillshade-highlight-color":rgba(c.line,0.22),"hillshade-shadow-color":"rgba(2,5,16,0.55)","hillshade-accent-color":rgba(c.glow,0.10)}},
      {id:"holo-osm-water",type:"line",source:"osm","source-layer":"water",minzoom:5,layout:line,paint:{"line-color":c.line,"line-width":["interpolate",["linear"],["zoom"],5,0.7,12,1.2],"line-opacity":fadeZ(5,7.5,0.8)}},
      {id:"holo-osm-waterway",type:"line",source:"osm","source-layer":"waterway",minzoom:7,layout:line,paint:{"line-color":c.detail,"line-width":0.7,"line-opacity":fadeZ(7,9,0.45)}},
      {id:"holo-osm-road",type:"line",source:"osm","source-layer":"transportation",minzoom:6,layout:line,filter:["match",["get","class"],["motorway","trunk","primary","secondary","tertiary","minor","street","service"],true,false],
        paint:{"line-color":c.detail,"line-width":["interpolate",["exponential",1.4],["zoom"],6,0.4,12,0.9,16,2.4],
          "line-opacity":["interpolate",["linear"],["zoom"],6,0,8,["match",["get","class"],["motorway","trunk","primary"],0.5,0],12,["match",["get","class"],["motorway","trunk","primary"],0.6,["secondary","tertiary"],0.45,0.3]]}},
      {id:"holo-osm-boundary",type:"line",source:"osm","source-layer":"boundary",minzoom:4,layout:line,filter:["all",["<=",["to-number",["get","admin_level"],99],4],["!=",["to-number",["get","maritime"],0],1]],
        paint:{"line-color":c.line,"line-width":["match",["to-number",["get","admin_level"],99],2,1.1,0.7],"line-dasharray":[3,2],"line-opacity":["interpolate",["linear"],["zoom"],4,0,6,["match",["to-number",["get","admin_level"],99],2,0.75,0.35]]}},
      {id:"holo-glow",type:"line",source:"holo-outlines",layout:line,paint:{"line-color":c.glow,"line-opacity":f(0.32),"line-blur":3,"line-width":["interpolate",["linear"],["zoom"],1,3.5,6,5]}},
      {id:"holo-fringe",type:"line",source:"holo-outlines",layout:line,paint:{"line-color":c.fringe,"line-opacity":f(0.35),"line-translate":[1.2,0.6],"line-width":["interpolate",["linear"],["zoom"],1,0.7,6,1]}},
      {id:"holo-line",type:"line",source:"holo-outlines",layout:line,paint:{"line-color":c.line,"line-opacity":f(0.95),"line-width":["interpolate",["linear"],["zoom"],1,0.8,6,1.2]}},
      {id:"holo-osm-building-line",type:"line",source:"osm","source-layer":"building",minzoom:13,layout:line,paint:{"line-color":c.line,"line-width":0.6,"line-opacity":fadeZ(13,14.5,0.55)}},
      {id:"holo-osm-building",type:"fill-extrusion",source:"osm","source-layer":"building",minzoom:13,paint:{"fill-extrusion-color":c.glow,"fill-extrusion-height":["coalesce",["get","render_height"],6],"fill-extrusion-base":["coalesce",["get","render_min_height"],0],"fill-extrusion-opacity":["interpolate",["linear"],["zoom"],13,0,14.5,0.28]}} ]; }
  // The hologram's outlines: each shared border drawn once, from the arcs of
  // the same world-atlas file the flat map's countries come from.
  function topoToLines(topo){ var sx=topo.transform.scale[0],sy=topo.transform.scale[1],tx=topo.transform.translate[0],ty=topo.transform.translate[1], lines=[];
    topo.arcs.forEach(function(arc){ var x=0,y=0,cur=[];
      for(var i=0;i<arc.length;i++){ x+=arc[i][0]; y+=arc[i][1]; var pt=[x*sx+tx,y*sy+ty], prev=cur[cur.length-1];
        if(prev&&((Math.abs(pt[0])>179.99&&Math.abs(prev[0])>179.99)||(pt[1]<-89.9&&prev[1]<-89.9)||Math.abs(pt[0]-prev[0])>180)){ if(cur.length>1) lines.push(cur); cur=[pt]; continue; }
        cur.push(pt); }
      if(cur.length>1) lines.push(cur); });
    return {type:"Feature",properties:{},geometry:{type:"MultiLineString",coordinates:lines}}; }
  function graticule(step){ var lines=[],lon,lat,l;
    for(lon=-180;lon<180;lon+=step){ l=[]; for(lat=-85;lat<=85;lat+=2) l.push([lon,lat]); l.push([lon,85]); lines.push(l); }
    for(lat=-75;lat<=75;lat+=step){ l=[]; for(lon=-180;lon<=180;lon+=2) l.push([lon,lat]); lines.push(l); }
    return {type:"Feature",properties:{},geometry:{type:"MultiLineString",coordinates:lines}}; }

  /* ---------- the map ---------- */
  var OPENING_ZOOM=1.35;
  var empty={type:"FeatureCollection",features:[]};
  var globe=new maplibregl.Map({
    container:"globeMap", renderWorldCopies:false, fadeDuration:0, maxPitch:85, rollEnabled:true,
    pixelRatio:Math.min(window.devicePixelRatio||1,1.5),
    center:[12,24], zoom:OPENING_ZOOM, minZoom:0.4,
    attributionControl:{compact:true},
    style:{ version:8, projection:{type:"vertical-perspective"}, sky:SKY_DAY,
      glyphs:"https://welcometoyourgalaxy.github.io/culprits/glyphs/{fontstack}/{range}.pbf",
      sources:{
        base:{type:"raster",tiles:["https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{z}/{y}/{x}"],tileSize:256,maxzoom:18,attribution:"Imagery © Esri, Maxar"},
        hillshade:{type:"raster",tiles:["https://services.arcgisonline.com/arcgis/rest/services/Elevation/World_Hillshade/MapServer/tile/{z}/{y}/{x}"],tileSize:256,maxzoom:16,attribution:"Hillshade © Esri"},
        labels:{type:"raster",tiles:["https://a.basemaps.cartocdn.com/rastertiles/voyager_only_labels/{z}/{x}/{y}@2x.png?key=cb1_494p_1_eebbbfcb65bc573e54783d42"],tileSize:256,attribution:"Labels © CARTO, © OpenStreetMap"},
        "holo-labels":{type:"raster",tiles:["https://a.basemaps.cartocdn.com/rastertiles/dark_only_labels/{z}/{x}/{y}@2x.png?key=cb1_494p_1_eebbbfcb65bc573e54783d42"],tileSize:256,attribution:"Labels © CARTO, © OpenStreetMap"},
        "plate-base":{type:"image",url:(typeof PLATE_IMG==="string"&&PLATE_IMG)?PLATE_IMG:"https://welcometoyourgalaxy.github.io/culprits/atlas-plate.webp",
          coordinates:[[-180,PLATE.top],[180,PLATE.top],[180,PLATE.bot],[-180,PLATE.bot]]},
        "night-lights":{type:"raster",tiles:["gmonight://{z}/{y}/{x}"],tileSize:256,maxzoom:8,attribution:'<a href="https://earthobservatory.nasa.gov/features/NightLights" target="_blank" rel="noopener">NASA Black Marble 2016</a> via GIBS'},
        osm:OSM_SOURCE, "outline-dem":RELIEF_SOURCE, "sea-dem":TERRAIN_SOURCE, "world-sheet":WORLD_SHEET,
        countries:{type:"geojson",data:empty,promoteId:"id"},
        "holo-outlines":{type:"geojson",data:empty,tolerance:0.2},
        "holo-graticule":{type:"geojson",data:graticule(15)},
        points:{type:"geojson",data:empty}
      },
      layers:[
        {id:"bg",type:"background",paint:{"background-color":"#0B1017"}},
        {id:"base",type:"raster",source:"base",paint:Object.assign({"raster-opacity":1},BASE_GRADE.atlas)},
        {id:"hillshade",type:"raster",source:"hillshade",paint:{"raster-opacity":["interpolate",["linear"],["zoom"],4,.18,9,.34,13,.46]}}
      ] }
  });
  window.gmoGlobe=globe;
  // The planet sits in the room the side columns leave, not under them.
  function fitPadding(){
    try{ var w=window.innerWidth, h=window.innerHeight, sb=document.getElementById("sidebar"), rb=document.getElementById("rightbar"), ip=document.getElementById("infoPanel");
      var left=0, right=0; [sb,ip].forEach(function(el){ if(el&&el.offsetWidth){ var r=el.getBoundingClientRect(); if(r.left<w/2) left=Math.max(left,r.right); } });
      if(rb&&rb.offsetWidth){ var rr=rb.getBoundingClientRect(); right=Math.max(0,w-rr.left); }
      if(w<900){ left=0; right=0; }
      globe.setPadding({left:Math.min(left,w*0.45),right:Math.min(right,w*0.3),top:60,bottom:Math.min(ctl.offsetHeight+20,h*0.25)}); }catch(e){}
  }
  window.addEventListener("resize",fitPadding);
  var hide=function(l){ l.layout=Object.assign({},l.layout||{},{visibility:"none"}); return l; };
  var show=function(id,on){ if(globe.getLayer(id)) globe.setLayoutProperty(id,"visibility",on?"visible":"none"); };
  var LAYERS_BY_BASEMAP={};
  var holoOn=false;

  globe.on("load",function(){
    // Jurassic's relief, drawn above the photograph.
    [ {id:"sat-relief-colour",type:"color-relief",source:"outline-dem",paint:{"color-relief-color":SAT_RELIEF.colour,"color-relief-opacity":1}},
      {id:"sat-relief-seabed",type:"color-relief",source:"sea-dem",paint:{"color-relief-color":SAT_RELIEF.seabed,"color-relief-opacity":1}},
      {id:"sat-relief-shade",type:"hillshade",source:"outline-dem",paint:SAT_RELIEF.shade},
      {id:"sat-relief-depth",type:"hillshade",source:"outline-dem",paint:SAT_RELIEF.depth},
      {id:"sat-relief-sea",type:"color-relief",source:"sea-dem",paint:{"color-relief-color":SAT_RELIEF.sea,"color-relief-opacity":1}}
    ].forEach(function(l){ try{ globe.addLayer(hide(l)); }catch(e){ console.warn("[globe] jurassic relief:",e.message||e); } });
    LAYERS_BY_BASEMAP.jurassic=["base","hillshade","sat-relief-colour","sat-relief-seabed","sat-relief-shade","sat-relief-depth","sat-relief-sea"];
    // The washes and the plate go UNDER the hillshade, not over it as on the
    // Culprits map: MapLibre 5.24's globe draws a raster layer at full
    // strength when the layer before it was a part-transparent raster whose
    // tiles go deeper than its own, so plate-after-hillshade never faded.
    // Hillshade-after-plate does, and the hillshade is kept off until the
    // plate has gone (the chart carries its own drawn relief).
    try{ globe.addLayer(atlasWashes,"hillshade"); }catch(e){ console.warn("[globe] atlas washes:",e.message||e); }
    globe.addLayer({id:"plate-base",type:"raster",source:"plate-base",paint:{"raster-opacity":["interpolate",["linear"],["zoom"],PLATE.fadeIn,1,PLATE.fadeOut,0],"raster-fade-duration":0}},"hillshade");
    globe.setPaintProperty("hillshade","raster-opacity",["interpolate",["linear"],["zoom"],PLATE.fadeIn,0,PLATE.fadeOut,.2,9,.34,13,.46]);
    LAYERS_BY_BASEMAP.atlas=["base","hillshade","plate-base"];
    var add=function(list,key){ var ids=[]; list.forEach(function(l){ try{ globe.addLayer(hide(l)); ids.push(l.id); }catch(e){ console.warn("[globe] "+key+" layer "+l.id+":",e.message||e); } }); return ids; };
    LAYERS_BY_BASEMAP.outlines=add(outlineLayers(),"standard");
    LAYERS_BY_BASEMAP.hell=add(hellLayers(),"hell").concat(add(hellNameLayers(),"hell names"));
    LAYERS_BY_BASEMAP.night=add(nightLayers(),"night");
    LAYERS_BY_BASEMAP.holo=add(holoLayers(),"hologram");
    globe.addLayer({id:"labels",type:"raster",source:"labels",paint:{"raster-opacity":.92}});
    globe.addLayer(hide({id:"holo-labels",type:"raster",source:"holo-labels",paint:{"raster-opacity":0.85,"raster-saturation":-1,"raster-fade-duration":0}}));
    // Countries: a see-through sheet to click on, and a faint edge where the
    // basemap draws none of its own.
    globe.addLayer({id:"gl-countries-fill",type:"fill",source:"countries",paint:{"fill-color":"#ffffff","fill-opacity":0.01}});
    globe.addLayer({id:"gl-countries-hover",type:"line",source:"countries",paint:{"line-color":"rgba(223,231,245,0.75)","line-width":1.6,"line-opacity":["case",["boolean",["feature-state","hover"],false],1,0]}});
    globe.addLayer(hide({id:"gl-countries-line",type:"line",source:"countries",paint:{"line-color":"rgba(223,231,245,0.22)","line-width":["interpolate",["linear"],["zoom"],1,.5,5,.9]}}));
    // The markers: the same points, colours and sizes the flat map draws.
    // Radius by zoom, scaled by the record's impact grade, as pjRad() does on
    // the flat map. MapLibre wants zoom at the top of the expression.
    var imp=["match",["get","i"],5,1.7,4,1.45,3,1.25,2,1.08,1];
    var rad=function(k){ var e=["interpolate",["linear"],["zoom"]]; [[0,1.5],[3,2.2],[5,3.2],[7,4.4],[9,5.6],[12,7]].forEach(function(s){ e.push(s[0],["*",s[1]*k,imp]); }); return e; };
    globe.addLayer({id:"pt-glow",type:"circle",source:"points",paint:{"circle-color":["get","c"],"circle-opacity":0.28,"circle-blur":1,"circle-radius":rad(2.4)}});
    globe.addLayer({id:"pt-core",type:"circle",source:"points",paint:{"circle-color":["get","c"],"circle-opacity":0.95,"circle-radius":rad(1),"circle-stroke-color":"rgba(8,12,27,0.85)","circle-stroke-width":0.8}});
    fetch("https://cdn.jsdelivr.net/npm/world-atlas@2/countries-50m.json").then(function(r){ return r.json(); })
      .then(function(topo){ var s=globe.getSource("holo-outlines"); if(s) s.setData(topoToLines(topo)); })
      .catch(function(e){ console.warn("[globe] hologram outlines:",e.message||e); });
    setBasemap(BASEMAP);
    fitPadding(); globe.jumpTo({center:[12,24],zoom:OPENING_ZOOM});
    feedPoints(); feedCountries();
  });

  /* ---------- basemaps on and off ---------- */
  function setBasemap(kind){
    if(!BASEMAPS.some(function(b){ return b[0]===kind; })) kind="atlas";
    BASEMAP=kind; try{ localStorage.setItem(BM_KEY,kind); }catch(e){}
    Array.prototype.forEach.call(ctl.querySelectorAll("button.bm"),function(b){ b.classList.toggle("on",b.dataset.bm===kind); });
    if(!globe.isStyleLoaded||!globe.getLayer("labels")) return;
    Object.keys(LAYERS_BY_BASEMAP).forEach(function(k){ LAYERS_BY_BASEMAP[k].forEach(function(id){ show(id,false); }); });
    (LAYERS_BY_BASEMAP[kind]||[]).forEach(function(id){ show(id,true); });
    if(kind==="atlas"||kind==="jurassic"){ Object.keys(BASE_GRADE[kind]).forEach(function(k){ globe.setPaintProperty("base",k,BASE_GRADE[kind][k]); }); }
    show("bg",true);
    holoOn=(kind==="holo"); box.classList.toggle("holo-on",holoOn);
    show("holo-labels",holoOn); show("labels",!holoOn&&kind!=="hell");
    show("gl-countries-line",kind==="jurassic");
    if(globe.getLayer("labels")){
      globe.setPaintProperty("labels","raster-opacity",kind==="atlas"?["interpolate",["linear"],["zoom"],PLATE.fadeIn,0,PLATE.fadeOut,.92]:kind==="jurassic"?.8:.92);
      globe.setPaintProperty("labels","raster-saturation",kind==="jurassic"||kind==="night"||kind==="outlines"?-1:0);
      globe.setPaintProperty("labels","raster-brightness-min",kind==="night"||kind==="outlines"?0.8:0);
      globe.setPaintProperty("labels","raster-brightness-max",kind==="night"||kind==="outlines"?0.1:1); }
    try{ globe.setSky(kind==="night"?NIGHT.sky:kind==="holo"?SKY_HOLO:kind==="hell"?SKY_HELL:SKY_DAY); }catch(e){}
    globe.triggerRepaint(); drawRim();
  }

  /* ---------- the hologram's rim ---------- */
  var rim=box.querySelector(".holo-rim");
  function drawRim(){
    if(!rim) return; var w=box.clientWidth,h=box.clientHeight,dpr=window.devicePixelRatio||1;
    if(rim.width!==Math.round(w*dpr)||rim.height!==Math.round(h*dpr)){ rim.width=Math.round(w*dpr); rim.height=Math.round(h*dpr); }
    var g=rim.getContext("2d"); g.setTransform(dpr,0,0,dpr,0,0); g.clearRect(0,0,w,h);
    if(!holoOn) return;
    var cx=w/2,cy=h/2,R=20000,N=120,runs=[],run=[];
    for(var i=0;i<=N;i++){ var t=(i/N)*Math.PI*2, fx=cx+Math.cos(t)*R, fy=cy+Math.sin(t)*R, p=null;
      try{ p=globe.project(globe.unproject([fx,fy])); }catch(e){ p=null; }
      if(!p||!isFinite(p.x)||!isFinite(p.y)||Math.hypot(p.x-fx,p.y-fy)<2){ if(run.length>1) runs.push(run); run=[]; continue; }
      run.push(p); }
    if(run.length>1) runs.push(run); if(!runs.length) return;
    [[10,rgba(HOLO.glow,0.06)],[5,rgba(HOLO.glow,0.13)],[2.6,rgba(HOLO.line,0.3)],[1.3,rgba(HOLO.line,0.95)]].forEach(function(s){
      g.lineWidth=s[0]; g.strokeStyle=s[1]; g.lineJoin="round";
      runs.forEach(function(r){ g.beginPath(); g.moveTo(r[0].x,r[0].y); for(var k=1;k<r.length;k++) g.lineTo(r[k].x,r[k].y); g.stroke(); }); });
  }
  globe.on("render",function(){ if(holoOn) drawRim(); });
  globe.on("resize",function(){ drawRim(); });

  /* ---------- the markers, fed from the flat map's own filtered set ---------- */
  function feedPoints(){
    var pts=window.__pjPts||[], src=globe.getSource("points"); if(!src) return;
    var feats=[];
    for(var i=0;i<pts.length;i++){ var o=pts[i]; if(typeof o.la!=="number"||typeof o.lo!=="number") continue;
      feats.push({type:"Feature",properties:{k:i,c:o.c||"#9aa4c7",i:o.i||1,n:(o.p&&(o.p.name||o.p.title))||""},geometry:{type:"Point",coordinates:[o.lo,o.la]}}); }
    src.setData({type:"FeatureCollection",features:feats});
  }
  window.addEventListener("pj:rebuilt",feedPoints);
  function feedCountries(){
    var c=window.__gmoCountries, src=globe.getSource("countries"); if(!src) return;
    if(!c){ setTimeout(feedCountries,400); return; }
    // world-atlas carries each country's number as the feature's own id, a
    // string; MapLibre wants it as a numeric property to click and hover by.
    var feats=(c.features||[]).map(function(f){ return {type:"Feature",id:Number(f.id),properties:Object.assign({},f.properties||{},{id:Number(f.id)}),geometry:f.geometry}; });
    src.setData({type:"FeatureCollection",features:feats});
  }

  /* ---------- hovering, clicking, and dropping into the flat map ---------- */
  var tip=document.getElementById("globeTip"), hoverId=null;
  function setHover(id){ if(id===undefined||id===null||isNaN(id)) id=null; if(hoverId===id) return;
    if(hoverId!==null) try{ globe.setFeatureState({source:"countries",id:hoverId},{hover:false}); }catch(e){}
    hoverId=id; if(hoverId!==null) try{ globe.setFeatureState({source:"countries",id:hoverId},{hover:true}); }catch(e){} }
  function countryName(f){ var p=(f&&f.properties)||{}; return p.name||p.NAME||""; }
  globe.on("mousemove",function(e){
    var pts=globe.queryRenderedFeatures(e.point,{layers:["pt-glow","pt-core"]});
    if(pts.length){ setHover(null); globe.getCanvas().style.cursor="pointer";
      var names=[]; for(var i=0;i<pts.length&&names.length<4;i++){ var n=pts[i].properties.n; if(n&&names.indexOf(n)<0) names.push(n); }
      tip.innerHTML="<b>"+names.map(function(s){ return String(s).replace(/[<>&]/g,function(ch){ return {"<":"&lt;",">":"&gt;","&":"&amp;"}[ch]; }); }).join("<br>")+(pts.length>names.length?"<br>&hellip; "+pts.length+" records here":"")+"</b><span>Click to open on the flat map</span>";
      tip.style.display="block"; tip.style.left=(e.point.x+14)+"px"; tip.style.top=(e.point.y+10)+"px"; return; }
    var cs=globe.queryRenderedFeatures(e.point,{layers:["gl-countries-fill"]});
    if(cs.length){ setHover(cs[0].id); globe.getCanvas().style.cursor="pointer";
      tip.innerHTML="<b>"+countryName(cs[0])+"</b><span>Click to open on the flat map</span>";
      tip.style.display="block"; tip.style.left=(e.point.x+14)+"px"; tip.style.top=(e.point.y+10)+"px"; return; }
    setHover(null); globe.getCanvas().style.cursor=""; tip.style.display="none";
  });
  globe.on("mouseout",function(){ setHover(null); tip.style.display="none"; });
  var dragged=false; globe.on("dragstart",function(){ dragged=true; }); globe.on("dragend",function(){ setTimeout(function(){ dragged=false; },50); });
  globe.on("click",function(e){
    if(dragged) return;
    var pts=globe.queryRenderedFeatures(e.point,{layers:["pt-glow","pt-core"]});
    if(pts.length){ var o=(window.__pjPts||[])[pts[0].properties.k]; if(!o) return;
      var lz=Math.max(6,Math.round(globe.getZoom()+1));
      toFlat([o.la,o.lo],lz,function(){ if(typeof window.pjGlobeOpen==="function") window.pjGlobeOpen(o); }); return; }
    var cs=globe.queryRenderedFeatures(e.point,{layers:["gl-countries-fill"]});
    if(cs.length){ var id=cs[0].id, feat=null, list=(window.__gmoCountries&&window.__gmoCountries.features)||[];
      for(var i=0;i<list.length;i++){ if(String(list[i].id)===String(id)){ feat=list[i]; break; } }
      var ll=[e.lngLat.lat,e.lngLat.lng];
      toFlat(ll,Math.max(3,Math.round(globe.getZoom()+1)),function(){ try{ if(feat&&typeof window.__gmoBaseClick==="function") window.__gmoBaseClick(feat,L.latLng(ll[0],ll[1])); }catch(err){ console.warn("[globe] country open:",err.message||err); } }); }
  });

  /* ---------- the two views ---------- */
  var VIEW="globe";
  var bGlobe=document.getElementById("gbViewGlobe"), bFlat=document.getElementById("gbViewFlat");
  function flatMap(){ return (typeof map!=="undefined"&&map&&typeof map.setView==="function")?map:null; }
  function toFlat(center,zoom,after){
    var m=flatMap(); VIEW="flat";
    bGlobe.classList.remove("on"); bFlat.classList.add("on");
    if(!center&&m){ var c=globe.getCenter(); center=[c.lat,c.lng]; zoom=Math.max(2,Math.round(globe.getZoom()+1)); }
    document.body.classList.remove("globe-on"); box.classList.add("off"); tip.style.display="none";
    if(m){ try{ m.invalidateSize(false); }catch(e){} try{ if(center) m.setView(center,zoom,{animate:false}); }catch(e){} }
    document.getElementById("gbBasemaps").style.display="none"; document.querySelector("#globeBox .gb-zoom").style.display="none"; document.getElementById("gbWorld").style.display="none";
    if(after) setTimeout(after,80);
  }
  function toGlobe(){
    var m=flatMap(); VIEW="globe";
    bFlat.classList.remove("on"); bGlobe.classList.add("on");
    if(m){ try{ var c=m.getCenter(); globe.jumpTo({center:[c.lng,c.lat],zoom:Math.max(0.4,m.getZoom()-1),pitch:0,bearing:0}); }catch(e){} }
    document.body.classList.add("globe-on"); box.classList.remove("off");
    document.getElementById("gbBasemaps").style.display=""; document.querySelector("#globeBox .gb-zoom").style.display=""; document.getElementById("gbWorld").style.display="";
    setTimeout(function(){ try{ globe.resize(); }catch(e){} },30);
  }
  window.gmoToFlat=toFlat; window.gmoToGlobe=toGlobe;
  bGlobe.addEventListener("click",function(){ if(VIEW!=="globe") toGlobe(); });
  bFlat.addEventListener("click",function(){ if(VIEW!=="flat") toFlat(); });
  document.getElementById("gbBasemaps").addEventListener("click",function(e){ var b=e.target.closest&&e.target.closest("button.bm"); if(b) setBasemap(b.dataset.bm); });
  document.getElementById("gbZoomIn").addEventListener("click",function(){ globe.zoomIn(); });
  document.getElementById("gbZoomOut").addEventListener("click",function(){ globe.zoomOut(); });
  document.getElementById("gbWorld").addEventListener("click",function(){ fitPadding(); globe.easeTo({center:[globe.getCenter().lng,20],zoom:OPENING_ZOOM,pitch:0,bearing:0,roll:0,duration:900}); });

  // The globe is the opening view.
  document.body.classList.add("globe-on");
})();
</script>
<!-- ====================================================== end of the globe -->
"""

edits = [
    # 1. Publish the filtered marker set every time the flat map rebuilds it.
    (
        "    _pjPts=pts; _pjGrid=grid; _pjShown=pts.length; _pjClu=null; _pjCluZ=null; return pts.length;",
        "    _pjPts=pts; _pjGrid=grid; _pjShown=pts.length; _pjClu=null; _pjCluZ=null;\n"
        "    try{ window.__pjPts=pts; window.dispatchEvent(new CustomEvent('pj:rebuilt')); }catch(_e){}\n"
        "    return pts.length;",
    ),
    # 2. Open one marker's popup from outside, the way a click on the dot does.
    (
        "  var ProjectLayer=L.Layer.extend({",
        "  window.pjGlobeOpen=function(o){ if(!o||!o.p) return;\n"
        "    try{ if(window.pjDrill && window.pjDrill(o.p)){ if(_pjPopup) map.closePopup(_pjPopup); return; } }catch(_e){}\n"
        "    if(!_pjPopup)_pjPopup=L.popup({maxWidth:320,autoPan:true});\n"
        "    _pjPopup.setLatLng([o.la,o.lo]).setContent(pjPopupHtml(o.p)).openOn(map); try{ pjEnrich(o.p); }catch(_e){}\n"
        "    try{ if(window.pjShowRecords) window.pjShowRecords(o.p); }catch(_e){} };\n"
        "  var ProjectLayer=L.Layer.extend({",
    ),
    # 3. The country shapes and the country click, for the globe to reuse.
    (
        "  geojsonLayer=L.geoJson(countries,{style:baseStyle,onEachFeature:baseOnEach,smoothFactor:1.6,coordsToLatLng:c=>L.latLng(c[1],c[0])}).addTo(map);",
        "  geojsonLayer=L.geoJson(countries,{style:baseStyle,onEachFeature:baseOnEach,smoothFactor:1.6,coordsToLatLng:c=>L.latLng(c[1],c[0])}).addTo(map);\n"
        "  window.__gmoCountries=countries; window.__gmoBaseClick=baseClick;",
    ),
    # 4. The globe itself, at the foot of the page.
    (
        "\n</body>",
        "\n" + BLOCK + "</body>",
    ),
]
for old, new in edits:
    n = s.count(old)
    if n != 1:
        sys.exit(f"expected exactly one match, found {n}:\n  {old[:100]}")
    s = s.replace(old, new)

P.write_text(s, encoding="utf-8")
print("applied: the globe is the opening view; six basemaps; Flat map on the toggle")
