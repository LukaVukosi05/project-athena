(function(){
 const esc=value=>escapeWhiteboardHtml(value);
 const level=(state,phase)=>{const a=(state.annotations||[]).find(x=>String(x).startsWith("visual-stage:"));const n=a?Number(a.split(":")[1]):0;return phase==="result"?n+1:n;};
 const frame=(p,phase,svg,text)=>{const ids=p.objects;return '<figure class="coordinate-native '+phase+'" data-managed-visibility="true"><div data-object-id="'+ids[0]+'" class="semantic-object is-visible">'+svg+'</div><p data-object-id="'+ids[1]+'" class="semantic-object '+(phase==="ready"?"is-hidden":"is-visible")+'">Construct from the signed coordinates.</p><p data-object-id="'+ids[2]+'" class="semantic-object '+(phase==="result"?"is-visible":"is-hidden")+'">'+esc(text)+'</p></figure>';};
 function distance(p,state,phase){const n=level(state,phase),xs=p.x_values,ys=p.y_values,minX=Math.min(0,...xs)-1,maxX=Math.max(0,...xs)+1,minY=Math.min(0,...ys)-1,maxY=Math.max(0,...ys)+1,sx=x=>50+(x-minX)/(maxX-minX)*460,sy=y=>155-(y-minY)/(maxY-minY)*125;const points=n?xs.map((x,i)=>'<g><circle cx="'+sx(x)+'" cy="'+sy(ys[i])+'" r="6"/><text x="'+(sx(x)+8)+'" y="'+(sy(ys[i])-8)+'">'+esc(p.labels[i])+'('+x+', '+ys[i]+')</text></g>').join(""):"";const construction=n>=2?'<line x1="'+sx(xs[0])+'" y1="'+sy(ys[0])+'" x2="'+sx(xs[1])+'" y2="'+sy(ys[1])+'"/><path d="M '+sx(xs[0])+' '+sy(ys[0])+' H '+sx(xs[1])+' V '+sy(ys[1])+'"/><text x="'+((sx(xs[0])+sx(xs[1]))/2)+'" y="'+(sy(ys[0])+18)+'">Δx='+p.delta_x+'</text><text x="'+(sx(xs[1])+8)+'" y="'+((sy(ys[0])+sy(ys[1]))/2)+'">Δy='+p.delta_y+'</text>':"";return frame(p,phase,'<svg viewBox="0 0 560 190" role="img"><title>Coordinate distance construction</title><desc>Points '+p.labels[0]+' at '+xs[0]+', '+ys[0]+' and '+p.labels[1]+' at '+xs[1]+', '+ys[1]+', with displacement '+p.delta_x+', '+p.delta_y+'.</desc><line x1="30" y1="'+sy(0)+'" x2="535" y2="'+sy(0)+'"/><line x1="'+sx(0)+'" y1="15" x2="'+sx(0)+'" y2="175"/>'+points+construction+'</svg>','Displacement ('+p.delta_x+', '+p.delta_y+')');}
 function circle(p,state,phase){const n=level(state,phase),scale=12,cx=280+p.centre_x*scale,cy=100-p.centre_y*scale,r=p.radius*scale;const centre=n?'<circle cx="'+cx+'" cy="'+cy+'" r="6"/><text x="'+(cx+8)+'" y="'+(cy-8)+'">C('+p.centre_x+', '+p.centre_y+')</text>':"";const shape=n>=2?'<circle cx="'+cx+'" cy="'+cy+'" r="'+r+'" class="circle-shape"/><line x1="'+cx+'" y1="'+cy+'" x2="'+(cx+r)+'" y2="'+cy+'"/><text x="'+(cx+r/2)+'" y="'+(cy-8)+'">r='+p.radius+'</text>':"";return frame(p,phase,'<svg viewBox="0 0 560 200" role="img"><title>Circle from centre and radius</title><desc>Circle centred at '+p.centre_x+', '+p.centre_y+' with radius '+p.radius+'.</desc><line x1="30" y1="100" x2="530" y2="100"/><line x1="280" y1="15" x2="280" y2="185"/>'+centre+shape+'</svg>','Centre ('+p.centre_x+', '+p.centre_y+'); radius '+p.radius);}
 function nativeScene(template,p,state,phase){
  const fmt=value=>Number.isInteger(value)?String(value):Number(value).toFixed(3).replace(/0+$/,"").replace(/\.$/,"");
  const n=level(state,phase),xs=p.x_values,ys=p.y_values;
  const extraX=[p.midpoint_x,p.centre_x].filter(Number.isFinite),extraY=[p.midpoint_y,p.centre_y].filter(Number.isFinite);
  const radius=Number.isFinite(p.radius)?p.radius:0;
  const minX=Math.min(0,...xs,...extraX,...extraX.map(x=>x-radius))-2,maxX=Math.max(0,...xs,...extraX,...extraX.map(x=>x+radius))+2;
  const minY=Math.min(0,...ys,...extraY,...extraY.map(y=>y-radius))-2,maxY=Math.max(0,...ys,...extraY,...extraY.map(y=>y+radius))+2;
  const sx=x=>42+(x-minX)/(maxX-minX)*478,sy=y=>174-(y-minY)/(maxY-minY)*146;
  let construction="";
  const points=n&&template!=="external_tangent_length"?xs.map((x,index)=>'<g class="coordinate-point"><circle cx="'+sx(x)+'" cy="'+sy(ys[index])+'" r="5"/><text x="'+(sx(x)+7)+'" y="'+(sy(ys[index])-7)+'">'+esc(p.labels[index])+'('+x+', '+ys[index]+')</text></g>').join(""):"";
  if(n>=2&&xs.length>=2){
   construction+='<line class="coordinate-segment" x1="'+sx(xs[0])+'" y1="'+sy(ys[0])+'" x2="'+sx(xs[1])+'" y2="'+sy(ys[1])+'"/>';
   if(["slope_triangle","coordinate_distance_lab"].includes(template))construction+='<path class="coordinate-construction" d="M '+sx(xs[0])+' '+sy(ys[0])+' H '+sx(xs[1])+' V '+sy(ys[1])+'"/>';
  }
  if(n>=2&&Number.isFinite(p.midpoint_x))construction+='<g class="midpoint-marker"><circle cx="'+sx(p.midpoint_x)+'" cy="'+sy(p.midpoint_y)+'" r="6"/><text x="'+(sx(p.midpoint_x)+8)+'" y="'+(sy(p.midpoint_y)-8)+'">M('+p.midpoint_x+', '+p.midpoint_y+')</text></g>';
  if(n>=2&&Number.isFinite(p.gradient)&&!["inclination_arc"].includes(template)){
   const anchorX=xs[0]||0,anchorY=ys[0]||0,x1=minX+1,x2=maxX-1,y1=anchorY+p.gradient*(x1-anchorX),y2=anchorY+p.gradient*(x2-anchorX);
   construction+='<line class="equation-line" x1="'+sx(x1)+'" y1="'+sy(y1)+'" x2="'+sx(x2)+'" y2="'+sy(y2)+'"/><text x="48" y="22">m='+fmt(p.gradient)+'</text>';
   if(Number.isFinite(p.secondary_gradient)){
    const tangentIndex=Math.min(1,xs.length-1),tx=xs[tangentIndex],ty=ys[tangentIndex],ty1=ty+p.secondary_gradient*(x1-tx),ty2=ty+p.secondary_gradient*(x2-tx);
    construction+='<line class="tangent-line" x1="'+sx(x1)+'" y1="'+sy(ty1)+'" x2="'+sx(x2)+'" y2="'+sy(ty2)+'"/><text x="48" y="40">m₂='+fmt(p.secondary_gradient)+'</text>';
   }
  }
  if(n>=2&&template==="inclination_arc"){
   const angle=Number.isFinite(p.inclination)?p.inclination:(Math.atan(p.gradient)*180/Math.PI+180)%180,r=58,cx=sx(0),cy=sy(0),endX=cx+r*Math.cos(angle*Math.PI/180),endY=cy-r*Math.sin(angle*Math.PI/180);
   construction+='<line class="inclination-ray" x1="'+cx+'" y1="'+cy+'" x2="'+endX+'" y2="'+endY+'"/><path class="inclination-marker" d="M '+(cx+r)+' '+cy+' A '+r+' '+r+' 0 0 0 '+endX+' '+endY+'"/><text x="'+(cx+65)+'" y="'+(cy-16)+'">θ='+angle+'°</text>';
  }
  if(n>=2&&Number.isFinite(p.centre_x)&&Number.isFinite(p.radius)){
   const radiusPixels=Math.min(Math.abs(sx(p.centre_x+p.radius)-sx(p.centre_x)),Math.abs(sy(p.centre_y+p.radius)-sy(p.centre_y)));
   construction+='<circle class="circle-shape" cx="'+sx(p.centre_x)+'" cy="'+sy(p.centre_y)+'" r="'+radiusPixels+'"/><circle class="circle-centre" cx="'+sx(p.centre_x)+'" cy="'+sy(p.centre_y)+'" r="5"/><text x="'+(sx(p.centre_x)+7)+'" y="'+(sy(p.centre_y)-7)+'">C('+p.centre_x+', '+p.centre_y+'), r='+p.radius+'</text>';
  }
  if(n>=1&&template==="external_tangent_length"){
   const op=Number.isFinite(p.op_distance)?p.op_distance:1,rad=Number.isFinite(p.radius)?p.radius:1,tangent=Number.isFinite(p.tangent_length)?p.tangent_length:Math.sqrt(Math.max(0,op*op-rad*rad));
   construction+='<path class="radius-and-op" d="M 130 150 L 130 55 L 390 150"/><text x="72" y="105">r='+rad+'</text><text x="255" y="92">OP='+op+'</text>';
   if(n>=2)construction+='<line class="tangent-segment" x1="130" y1="150" x2="390" y2="150"/><path class="right-angle-marker" d="M 130 135 H 145 V 150"/><text x="235" y="170">PT='+tangent+'</text>';
  }
  if(n>=2&&template==="coordinate_proof_studio"&&xs.length>=4)construction+='<polygon class="proof-polygon" fill="none" points="'+xs.map((x,index)=>sx(x)+','+sy(ys[index])).join(' ')+'"/><path class="right-angle-marker" d="M '+(sx(xs[0])+12)+' '+sy(ys[0])+' v -12 h -12"/>';
  const summary=template==="external_tangent_length"?'OP '+p.op_distance+'; radius '+p.radius+'; tangent length '+p.tangent_length:Number.isFinite(p.midpoint_x)?'Midpoint ('+p.midpoint_x+', '+p.midpoint_y+')':Number.isFinite(p.radius)?'Centre ('+p.centre_x+', '+p.centre_y+'); radius '+p.radius:p.result;
  const svg='<svg viewBox="0 0 560 205" role="img"><title>'+esc(p.title||template.replaceAll('_',' '))+'</title><desc>Question-specific analytical geometry construction using '+p.labels.map((label,index)=>label+' at '+xs[index]+', '+ys[index]).join('; ')+'.</desc><line class="coordinate-axis" x1="24" y1="'+sy(0)+'" x2="536" y2="'+sy(0)+'"/><line class="coordinate-axis" x1="'+sx(0)+'" y1="12" x2="'+sx(0)+'" y2="190"/>'+points+construction+'</svg>';
  return frame(p,phase,svg,summary);
 }
 AthenaVisualizationRegistry.register("coordinate_geometry","coordinate_distance_lab",{render:distance});
 AthenaVisualizationRegistry.register("coordinate_geometry","circle_construction",{render:circle});
 ["midpoint_bisection","slope_triangle","line_equation_link","parallel_comparison","perpendicular_rotation","inclination_arc","complete_square_morph","circle_condition_intersection","radius_tangent_contact","tangent_equation_construction","external_tangent_length","coordinate_proof_studio","integrated_coordinate_scene","question_first_assessment"].forEach(template=>AthenaVisualizationRegistry.register("coordinate_geometry",template,{render:(parameters,state,phase)=>nativeScene(template,parameters,state,phase)}));
})();
