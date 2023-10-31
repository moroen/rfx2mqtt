import{c as ie,a as o,h as v,d as _e,g as ue,H as ct,r as w,v as E,B as Le,I as dt,J as F,n as vt,K as ft,L as X,M as te,N as xe,O as ae,P as K,R as ne,S as Te,j as mt,T as pt,U as V,V as bt,w as gt,W as ht,X as Ct,Y as kt,o as yt,Z as _t,$ as xt,a0 as wt,x as P,G as Y,y as N,a1 as re,C as le}from"./index.9dfe90e2.js";import{u as Be,a as St,b as $t,c as qt,d as Mt,e as Lt,f as R,g as Tt,h as Bt,p as we,Q as At}from"./use-quasar.2293db2a.js";import{Q as Et}from"./QPage.ed5bc905.js";import{api as Dt}from"./axios.e56d5bb1.js";import{u as Nt,d as zt}from"./scroll.a1e4ff81.js";var It=ie({name:"QTd",props:{props:Object,autoWidth:Boolean,noHover:Boolean},setup(t,{slots:a}){const l=ue(),s=o(()=>"q-td"+(t.autoWidth===!0?" q-table--col-auto-width":"")+(t.noHover===!0?" q-td--no-hover":"")+" ");return()=>{if(t.props===void 0)return v("td",{class:s.value},_e(a.default));const e=l.vnode.key,r=(t.props.colsMap!==void 0?t.props.colsMap[e]:null)||t.props.col;if(r===void 0)return;const{row:i}=t.props;return v("td",{class:s.value+r.__tdClass(i),style:r.__tdStyle(i)},_e(a.default))}}});const Rt=Be(),Ft={headers:{}};function Pt(t,a){Dt.get(t,Ft).then(l=>{a.value=l.data}).catch(()=>{Rt.notify({color:"negative",position:"top",message:"Loading failed",icon:"report_problem"})})}var Ae=ie({name:"QToggle",props:{...St,icon:String,iconColor:String},emits:$t,setup(t){function a(l,s){const e=o(()=>(l.value===!0?t.checkedIcon:s.value===!0?t.indeterminateIcon:t.uncheckedIcon)||t.icon),r=o(()=>l.value===!0?t.iconColor:null);return()=>[v("div",{class:"q-toggle__track"}),v("div",{class:"q-toggle__thumb absolute flex flex-center no-wrap"},e.value!==void 0?[v(ct,{name:e.value,color:r.value})]:void 0)]}return qt("toggle",a)}});const Vt={__name:"StateSwitch",props:["id","state"],setup(t){const l=w(t.state);return(s,e)=>(E(),Le(Ae,{modelValue:l.value,"onUpdate:modelValue":e[0]||(e[0]=r=>l.value=r)},null,8,["modelValue"]))}},ce={left:!0,right:!0,up:!0,down:!0,horizontal:!0,vertical:!0},Ot=Object.keys(ce);ce.all=!0;function Se(t){const a={};for(const l of Ot)t[l]===!0&&(a[l]=!0);return Object.keys(a).length===0?ce:(a.horizontal===!0?a.left=a.right=!0:a.left===!0&&a.right===!0&&(a.horizontal=!0),a.vertical===!0?a.up=a.down=!0:a.up===!0&&a.down===!0&&(a.vertical=!0),a.horizontal===!0&&a.vertical===!0&&(a.all=!0),a)}const jt=["INPUT","TEXTAREA"];function $e(t,a){return a.event===void 0&&t.target!==void 0&&t.target.draggable!==!0&&typeof a.handler=="function"&&jt.includes(t.target.nodeName.toUpperCase())===!1&&(t.qClonedBy===void 0||t.qClonedBy.indexOf(a.uid)===-1)}function oe(t,a,l){const s=K(t);let e,r=s.left-a.event.x,i=s.top-a.event.y,c=Math.abs(r),p=Math.abs(i);const d=a.direction;d.horizontal===!0&&d.vertical!==!0?e=r<0?"left":"right":d.horizontal!==!0&&d.vertical===!0?e=i<0?"up":"down":d.up===!0&&i<0?(e="up",c>p&&(d.left===!0&&r<0?e="left":d.right===!0&&r>0&&(e="right"))):d.down===!0&&i>0?(e="down",c>p&&(d.left===!0&&r<0?e="left":d.right===!0&&r>0&&(e="right"))):d.left===!0&&r<0?(e="left",c<p&&(d.up===!0&&i<0?e="up":d.down===!0&&i>0&&(e="down"))):d.right===!0&&r>0&&(e="right",c<p&&(d.up===!0&&i<0?e="up":d.down===!0&&i>0&&(e="down")));let _=!1;if(e===void 0&&l===!1){if(a.event.isFirst===!0||a.event.lastDir===void 0)return{};e=a.event.lastDir,_=!0,e==="left"||e==="right"?(s.left-=r,c=0,r=0):(s.top-=i,p=0,i=0)}return{synthetic:_,payload:{evt:t,touch:a.event.mouse!==!0,mouse:a.event.mouse===!0,position:s,direction:e,isFirst:a.event.isFirst,isFinal:l===!0,duration:Date.now()-a.event.time,distance:{x:c,y:p},offset:{x:r,y:i},delta:{x:s.left-a.event.lastX,y:s.top-a.event.lastY}}}}let Qt=0;var Ut=dt({name:"touch-pan",beforeMount(t,{value:a,modifiers:l}){if(l.mouse!==!0&&F.has.touch!==!0)return;function s(r,i){l.mouse===!0&&i===!0?Te(r):(l.stop===!0&&ae(r),l.prevent===!0&&xe(r))}const e={uid:"qvtp_"+Qt++,handler:a,modifiers:l,direction:Se(l),noop:vt,mouseStart(r){$e(r,e)&&ft(r)&&(X(e,"temp",[[document,"mousemove","move","notPassiveCapture"],[document,"mouseup","end","passiveCapture"]]),e.start(r,!0))},touchStart(r){if($e(r,e)){const i=r.target;X(e,"temp",[[i,"touchmove","move","notPassiveCapture"],[i,"touchcancel","end","passiveCapture"],[i,"touchend","end","passiveCapture"]]),e.start(r)}},start(r,i){if(F.is.firefox===!0&&te(t,!0),e.lastEvt=r,i===!0||l.stop===!0){if(e.direction.all!==!0&&(i!==!0||e.modifiers.mouseAllDir!==!0&&e.modifiers.mousealldir!==!0)){const d=r.type.indexOf("mouse")>-1?new MouseEvent(r.type,r):new TouchEvent(r.type,r);r.defaultPrevented===!0&&xe(d),r.cancelBubble===!0&&ae(d),Object.assign(d,{qKeyEvent:r.qKeyEvent,qClickOutside:r.qClickOutside,qAnchorHandled:r.qAnchorHandled,qClonedBy:r.qClonedBy===void 0?[e.uid]:r.qClonedBy.concat(e.uid)}),e.initialEvent={target:r.target,event:d}}ae(r)}const{left:c,top:p}=K(r);e.event={x:c,y:p,time:Date.now(),mouse:i===!0,detected:!1,isFirst:!0,isFinal:!1,lastX:c,lastY:p}},move(r){if(e.event===void 0)return;const i=K(r),c=i.left-e.event.x,p=i.top-e.event.y;if(c===0&&p===0)return;e.lastEvt=r;const d=e.event.mouse===!0,_=()=>{s(r,d);let k;l.preserveCursor!==!0&&l.preservecursor!==!0&&(k=document.documentElement.style.cursor||"",document.documentElement.style.cursor="grabbing"),d===!0&&document.body.classList.add("no-pointer-events--children"),document.body.classList.add("non-selectable"),Mt(),e.styleCleanup=b=>{if(e.styleCleanup=void 0,k!==void 0&&(document.documentElement.style.cursor=k),document.body.classList.remove("non-selectable"),d===!0){const z=()=>{document.body.classList.remove("no-pointer-events--children")};b!==void 0?setTimeout(()=>{z(),b()},50):z()}else b!==void 0&&b()}};if(e.event.detected===!0){e.event.isFirst!==!0&&s(r,e.event.mouse);const{payload:k,synthetic:b}=oe(r,e,!1);k!==void 0&&(e.handler(k)===!1?e.end(r):(e.styleCleanup===void 0&&e.event.isFirst===!0&&_(),e.event.lastX=k.position.left,e.event.lastY=k.position.top,e.event.lastDir=b===!0?void 0:k.direction,e.event.isFirst=!1));return}if(e.direction.all===!0||d===!0&&(e.modifiers.mouseAllDir===!0||e.modifiers.mousealldir===!0)){_(),e.event.detected=!0,e.move(r);return}const x=Math.abs(c),C=Math.abs(p);x!==C&&(e.direction.horizontal===!0&&x>C||e.direction.vertical===!0&&x<C||e.direction.up===!0&&x<C&&p<0||e.direction.down===!0&&x<C&&p>0||e.direction.left===!0&&x>C&&c<0||e.direction.right===!0&&x>C&&c>0?(e.event.detected=!0,e.move(r)):e.end(r,!0))},end(r,i){if(e.event!==void 0){if(ne(e,"temp"),F.is.firefox===!0&&te(t,!1),i===!0)e.styleCleanup!==void 0&&e.styleCleanup(),e.event.detected!==!0&&e.initialEvent!==void 0&&e.initialEvent.target.dispatchEvent(e.initialEvent.event);else if(e.event.detected===!0){e.event.isFirst===!0&&e.handler(oe(r===void 0?e.lastEvt:r,e).payload);const{payload:c}=oe(r===void 0?e.lastEvt:r,e,!0),p=()=>{e.handler(c)};e.styleCleanup!==void 0?e.styleCleanup(p):p()}e.event=void 0,e.initialEvent=void 0,e.lastEvt=void 0}}};if(t.__qtouchpan=e,l.mouse===!0){const r=l.mouseCapture===!0||l.mousecapture===!0?"Capture":"";X(e,"main",[[t,"mousedown","mouseStart",`passive${r}`]])}F.has.touch===!0&&X(e,"main",[[t,"touchstart","touchStart",`passive${l.capture===!0?"Capture":""}`],[t,"touchmove","noop","notPassiveCapture"]])},updated(t,a){const l=t.__qtouchpan;l!==void 0&&(a.oldValue!==a.value&&(typeof value!="function"&&l.end(),l.handler=a.value),l.direction=Se(a.modifiers))},beforeUnmount(t){const a=t.__qtouchpan;a!==void 0&&(a.event!==void 0&&a.end(),ne(a,"main"),ne(a,"temp"),F.is.firefox===!0&&te(t,!1),a.styleCleanup!==void 0&&a.styleCleanup(),delete t.__qtouchpan)}});const qe="q-slider__marker-labels",Xt=t=>({value:t}),Yt=({marker:t})=>v("div",{key:t.value,style:t.style,class:t.classes},t.label),Ee=[34,37,40,33,39,38],Kt={...zt,...Lt,min:{type:Number,default:0},max:{type:Number,default:100},innerMin:Number,innerMax:Number,step:{type:Number,default:1,validator:t=>t>=0},snap:Boolean,vertical:Boolean,reverse:Boolean,hideSelection:Boolean,color:String,markerLabelsClass:String,label:Boolean,labelColor:String,labelTextColor:String,labelAlways:Boolean,switchLabelSide:Boolean,markers:[Boolean,Number],markerLabels:[Boolean,Array,Object,Function],switchMarkerLabelsSide:Boolean,trackImg:String,trackColor:String,innerTrackImg:String,innerTrackColor:String,selectionColor:String,selectionImg:String,thumbSize:{type:String,default:"20px"},trackSize:{type:String,default:"4px"},disable:Boolean,readonly:Boolean,dense:Boolean,tabindex:[String,Number],thumbColor:String,thumbPath:{type:String,default:"M 4, 10 a 6,6 0 1,0 12,0 a 6,6 0 1,0 -12,0"}},Ht=["pan","update:modelValue","change"];function Gt({updateValue:t,updatePosition:a,getDragging:l,formAttrs:s}){const{props:e,emit:r,slots:i,proxy:{$q:c}}=ue(),p=Nt(e,c),d=Tt(s),_=w(!1),x=w(!1),C=w(!1),k=w(!1),b=o(()=>e.vertical===!0?"--v":"--h"),z=o(()=>"-"+(e.switchLabelSide===!0?"switched":"standard")),q=o(()=>e.vertical===!0?e.reverse===!0:e.reverse!==(c.lang.rtl===!0)),M=o(()=>isNaN(e.innerMin)===!0||e.innerMin<e.min?e.min:e.innerMin),L=o(()=>isNaN(e.innerMax)===!0||e.innerMax>e.max?e.max:e.innerMax),g=o(()=>e.disable!==!0&&e.readonly!==!0&&M.value<L.value),$=o(()=>(String(e.step).trim().split(".")[1]||"").length),B=o(()=>e.step===0?1:e.step),ze=o(()=>g.value===!0?e.tabindex||0:-1),O=o(()=>e.max-e.min),de=o(()=>L.value-M.value),j=o(()=>G(M.value)),H=o(()=>G(L.value)),Q=o(()=>e.vertical===!0?q.value===!0?"bottom":"top":q.value===!0?"right":"left"),ve=o(()=>e.vertical===!0?"height":"width"),Ie=o(()=>e.vertical===!0?"width":"height"),fe=o(()=>e.vertical===!0?"vertical":"horizontal"),Re=o(()=>{const n={role:"slider","aria-valuemin":M.value,"aria-valuemax":L.value,"aria-orientation":fe.value,"data-step":e.step};return e.disable===!0?n["aria-disabled"]="true":e.readonly===!0&&(n["aria-readonly"]="true"),n}),Fe=o(()=>`q-slider q-slider${b.value} q-slider--${_.value===!0?"":"in"}active inline no-wrap `+(e.vertical===!0?"row":"column")+(e.disable===!0?" disabled":" q-slider--enabled"+(g.value===!0?" q-slider--editable":""))+(C.value==="both"?" q-slider--focus":"")+(e.label||e.labelAlways===!0?" q-slider--label":"")+(e.labelAlways===!0?" q-slider--label-always":"")+(p.value===!0?" q-slider--dark":"")+(e.dense===!0?" q-slider--dense q-slider--dense"+b.value:""));function U(n){const u="q-slider__"+n;return`${u} ${u}${b.value} ${u}${b.value}${z.value}`}function me(n){const u="q-slider__"+n;return`${u} ${u}${b.value}`}const Pe=o(()=>{const n=e.selectionColor||e.color;return"q-slider__selection absolute"+(n!==void 0?` text-${n}`:"")}),Ve=o(()=>me("markers")+" absolute overflow-hidden"),Oe=o(()=>me("track-container")),je=o(()=>U("pin")),Qe=o(()=>U("label")),Ue=o(()=>U("text-container")),Xe=o(()=>U("marker-labels-container")+(e.markerLabelsClass!==void 0?` ${e.markerLabelsClass}`:"")),Ye=o(()=>"q-slider__track relative-position no-outline"+(e.trackColor!==void 0?` bg-${e.trackColor}`:"")),Ke=o(()=>{const n={[Ie.value]:e.trackSize};return e.trackImg!==void 0&&(n.backgroundImage=`url(${e.trackImg}) !important`),n}),He=o(()=>"q-slider__inner absolute"+(e.innerTrackColor!==void 0?` bg-${e.innerTrackColor}`:"")),pe=o(()=>{const n=H.value-j.value,u={[Q.value]:`${100*j.value}%`,[ve.value]:n===0?"2px":`${100*n}%`};return e.innerTrackImg!==void 0&&(u.backgroundImage=`url(${e.innerTrackImg}) !important`),u});function Ge(n){const{min:u,max:f,step:m}=e;let y=u+n*(f-u);if(m>0){const T=(y-u)%m;y+=(Math.abs(T)>=m/2?(T<0?-1:1)*m:0)-T}return $.value>0&&(y=parseFloat(y.toFixed($.value))),R(y,M.value,L.value)}function G(n){return O.value===0?0:(n-e.min)/O.value}function We(n,u){const f=K(n),m=e.vertical===!0?R((f.top-u.top)/u.height,0,1):R((f.left-u.left)/u.width,0,1);return R(q.value===!0?1-m:m,j.value,H.value)}const be=o(()=>pt(e.markers)===!0?e.markers:B.value),ge=o(()=>{const n=[],u=be.value,f=e.max;let m=e.min;do n.push(m),m+=u;while(m<f);return n.push(f),n}),he=o(()=>{const n=` ${qe}${b.value}-`;return qe+`${n}${e.switchMarkerLabelsSide===!0?"switched":"standard"}${n}${q.value===!0?"rtl":"ltr"}`}),W=o(()=>e.markerLabels===!1?null:Ze(e.markerLabels).map((n,u)=>({index:u,value:n.value,label:n.label||n.value,classes:he.value+(n.classes!==void 0?" "+n.classes:""),style:{...ke(n.value),...n.style||{}}}))),Ce=o(()=>({markerList:W.value,markerMap:et.value,classes:he.value,getStyle:ke})),Je=o(()=>{const n=de.value===0?"2px":100*be.value/de.value;return{...pe.value,backgroundSize:e.vertical===!0?`2px ${n}%`:`${n}% 2px`}});function Ze(n){if(n===!1)return null;if(n===!0)return ge.value.map(Xt);if(typeof n=="function")return ge.value.map(f=>{const m=n(f);return V(m)===!0?{...m,value:f}:{value:f,label:m}});const u=({value:f})=>f>=e.min&&f<=e.max;return Array.isArray(n)===!0?n.map(f=>V(f)===!0?f:{value:f}).filter(u):Object.keys(n).map(f=>{const m=n[f],y=Number(f);return V(m)===!0?{...m,value:y}:{value:y,label:m}}).filter(u)}function ke(n){return{[Q.value]:`${100*(n-e.min)/O.value}%`}}const et=o(()=>{if(e.markerLabels===!1)return null;const n={};return W.value.forEach(u=>{n[u.value]=u}),n});function tt(){if(i["marker-label-group"]!==void 0)return i["marker-label-group"](Ce.value);const n=i["marker-label"]||Yt;return W.value.map(u=>n({marker:u,...Ce.value}))}const at=o(()=>[[Ut,nt,void 0,{[fe.value]:!0,prevent:!0,stop:!0,mouse:!0,mouseAllDir:!0}]]);function nt(n){n.isFinal===!0?(k.value!==void 0&&(a(n.evt),n.touch===!0&&t(!0),k.value=void 0,r("pan","end")),_.value=!1,C.value=!1):n.isFirst===!0?(k.value=l(n.evt),a(n.evt),t(),_.value=!0,r("pan","start")):(a(n.evt),t())}function ye(){C.value=!1}function rt(n){a(n,l(n)),t(),x.value=!0,_.value=!0,document.addEventListener("mouseup",J,!0)}function J(){x.value=!1,_.value=!1,t(!0),ye(),document.removeEventListener("mouseup",J,!0)}function lt(n){a(n,l(n)),t(!0)}function ot(n){Ee.includes(n.keyCode)&&t(!0)}function st(n){if(e.vertical===!0)return null;const u=c.lang.rtl!==e.reverse?1-n:n;return{transform:`translateX(calc(${2*u-1} * ${e.thumbSize} / 2 + ${50-100*u}%))`}}function it(n){const u=o(()=>x.value===!1&&(C.value===n.focusValue||C.value==="both")?" q-slider--focus":""),f=o(()=>`q-slider__thumb q-slider__thumb${b.value} q-slider__thumb${b.value}-${q.value===!0?"rtl":"ltr"} absolute non-selectable`+u.value+(n.thumbColor.value!==void 0?` text-${n.thumbColor.value}`:"")),m=o(()=>({width:e.thumbSize,height:e.thumbSize,[Q.value]:`${100*n.ratio.value}%`,zIndex:C.value===n.focusValue?2:void 0})),y=o(()=>n.labelColor.value!==void 0?` text-${n.labelColor.value}`:""),T=o(()=>st(n.ratio.value)),Z=o(()=>"q-slider__text"+(n.labelTextColor.value!==void 0?` text-${n.labelTextColor.value}`:""));return()=>{const ee=[v("svg",{class:"q-slider__thumb-shape absolute-full",viewBox:"0 0 20 20","aria-hidden":"true"},[v("path",{d:e.thumbPath})]),v("div",{class:"q-slider__focus-ring fit"})];return(e.label===!0||e.labelAlways===!0)&&(ee.push(v("div",{class:je.value+" absolute fit no-pointer-events"+y.value},[v("div",{class:Qe.value,style:{minWidth:e.thumbSize}},[v("div",{class:Ue.value,style:T.value},[v("span",{class:Z.value},n.label.value)])])])),e.name!==void 0&&e.disable!==!0&&d(ee,"push")),v("div",{class:f.value,style:m.value,...n.getNodeData()},ee)}}function ut(n,u,f,m){const y=[];e.innerTrackColor!=="transparent"&&y.push(v("div",{key:"inner",class:He.value,style:pe.value})),e.selectionColor!=="transparent"&&y.push(v("div",{key:"selection",class:Pe.value,style:n.value})),e.markers!==!1&&y.push(v("div",{key:"marker",class:Ve.value,style:Je.value})),m(y);const T=[bt("div",{key:"trackC",class:Oe.value,tabindex:u.value,...f.value},[v("div",{class:Ye.value,style:Ke.value},y)],"slide",g.value,()=>at.value)];if(e.markerLabels!==!1){const Z=e.switchMarkerLabelsSide===!0?"unshift":"push";T[Z](v("div",{key:"markerL",class:Xe.value},tt()))}return T}return mt(()=>{document.removeEventListener("mouseup",J,!0)}),{state:{active:_,focus:C,preventFocus:x,dragging:k,editable:g,classes:Fe,tabindex:ze,attributes:Re,step:B,decimals:$,trackLen:O,innerMin:M,innerMinRatio:j,innerMax:L,innerMaxRatio:H,positionProp:Q,sizeProp:ve,isReversed:q},methods:{onActivate:rt,onMobileClick:lt,onBlur:ye,onKeyup:ot,getContent:ut,getThumbRenderFn:it,convertRatioToModel:Ge,convertModelToRatio:G,getDraggingRatio:We}}}const Wt=()=>({});var Jt=ie({name:"QSlider",props:{...Kt,modelValue:{required:!0,default:null,validator:t=>typeof t=="number"||t===null},labelValue:[String,Number]},emits:Ht,setup(t,{emit:a}){const{proxy:{$q:l}}=ue(),{state:s,methods:e}=Gt({updateValue:b,updatePosition:q,getDragging:z,formAttrs:Bt(t)}),r=w(null),i=w(0),c=w(0);function p(){c.value=t.modelValue===null?s.innerMin.value:R(t.modelValue,s.innerMin.value,s.innerMax.value)}gt(()=>`${t.modelValue}|${s.innerMin.value}|${s.innerMax.value}`,p),p();const d=o(()=>e.convertModelToRatio(c.value)),_=o(()=>s.active.value===!0?i.value:d.value),x=o(()=>{const g={[s.positionProp.value]:`${100*s.innerMinRatio.value}%`,[s.sizeProp.value]:`${100*(_.value-s.innerMinRatio.value)}%`};return t.selectionImg!==void 0&&(g.backgroundImage=`url(${t.selectionImg}) !important`),g}),C=e.getThumbRenderFn({focusValue:!0,getNodeData:Wt,ratio:_,label:o(()=>t.labelValue!==void 0?t.labelValue:c.value),thumbColor:o(()=>t.thumbColor||t.color),labelColor:o(()=>t.labelColor),labelTextColor:o(()=>t.labelTextColor)}),k=o(()=>s.editable.value!==!0?{}:l.platform.is.mobile===!0?{onClick:e.onMobileClick}:{onMousedown:e.onActivate,onFocus:M,onBlur:e.onBlur,onKeydown:L,onKeyup:e.onKeyup});function b(g){c.value!==t.modelValue&&a("update:modelValue",c.value),g===!0&&a("change",c.value)}function z(){return r.value.getBoundingClientRect()}function q(g,$=s.dragging.value){const B=e.getDraggingRatio(g,$);c.value=e.convertRatioToModel(B),i.value=t.snap!==!0||t.step===0?B:e.convertModelToRatio(c.value)}function M(){s.focus.value=!0}function L(g){if(!Ee.includes(g.keyCode))return;Te(g);const $=([34,33].includes(g.keyCode)?10:1)*s.step.value,B=([34,37,40].includes(g.keyCode)?-1:1)*(s.isReversed.value===!0?-1:1)*(t.vertical===!0?-1:1)*$;c.value=R(parseFloat((c.value+B).toFixed(s.decimals.value)),s.innerMin.value,s.innerMax.value),b()}return()=>{const g=e.getContent(x,s.tabindex,k,$=>{$.push(C())});return v("div",{ref:r,class:s.classes.value+(t.modelValue===null?" q-slider--no-value":""),...s.attributes.value,"aria-valuenow":t.modelValue},g)}}});let I,se,Me=0,A=null,h={},D={};const De={group:"__default_quasar_group__",delay:0,message:!1,html:!1,spinnerSize:80,spinnerColor:"",messageColor:"",backgroundColor:"",boxClass:"",spinner:wt,customClass:""},Ne={...De};function Zt(t){if(t&&t.group!==void 0&&D[t.group]!==void 0)return Object.assign(D[t.group],t);const a=V(t)===!0&&t.ignoreDefaults===!0?{...De,...t}:{...Ne,...t};return D[a.group]=a,a}const S=ht({isActive:!1},{show(t){h=Zt(t);const{group:a}=h;return S.isActive=!0,I!==void 0?(h.uid=Me,se.$forceUpdate()):(h.uid=++Me,A!==null&&clearTimeout(A),A=setTimeout(()=>{A=null;const l=Ct("q-loading");I=kt({name:"QLoading",setup(){yt(()=>{we(!0)});function s(){S.isActive!==!0&&I!==void 0&&(we(!1),I.unmount(l),xt(l),I=void 0,se=void 0)}function e(){if(S.isActive!==!0)return null;const r=[v(h.spinner,{class:"q-loading__spinner",color:h.spinnerColor,size:h.spinnerSize})];return h.message&&r.push(v("div",{class:"q-loading__message"+(h.messageColor?` text-${h.messageColor}`:""),[h.html===!0?"innerHTML":"textContent"]:h.message})),v("div",{class:"q-loading fullscreen flex flex-center z-max "+h.customClass.trim(),key:h.uid},[v("div",{class:"q-loading__backdrop"+(h.backgroundColor?` bg-${h.backgroundColor}`:"")}),v("div",{class:"q-loading__box column items-center "+h.boxClass},r)])}return()=>v(_t,{name:"q-transition--fade",appear:!0,onAfterLeave:s},e)}},S.__parentApp),se=I.mount(l)},h.delay)),l=>{if(l===void 0||Object(l)!==l){S.hide(a);return}S.show({...l,group:a})}},hide(t){if(S.isActive===!0){if(t===void 0)D={};else{if(D[t]===void 0)return;{delete D[t];const a=Object.keys(D);if(a.length!==0){const l=a[a.length-1];S.show({group:l});return}}}A!==null&&(clearTimeout(A),A=null),S.isActive=!1}},setDefaults(t){V(t)===!0&&Object.assign(Ne,t)},install({$q:t,parentApp:a}){t.loading=this,S.__parentApp=a,t.config.loading!==void 0&&this.setDefaults(t.config.loading)}}),ea={class:"q-pa-md example-row-equal-width"},ta={class:"row"},aa={class:"col"},na={class:"col"},ra={__name:"StateLight",props:["id","state","brightness"],setup(t){const a=t,l=w(a.state),s=w(a.brightness);return console.log(a),(e,r)=>(E(),P("div",ea,[Y("div",ta,[Y("div",aa,[N(Ae,{modelValue:l.value,"onUpdate:modelValue":r[0]||(r[0]=i=>l.value=i)},null,8,["modelValue"])]),Y("div",na,[N(Jt,{modelValue:s.value,"onUpdate:modelValue":r[1]||(r[1]=i=>s.value=i),min:0,max:100},null,8,["modelValue"])])])]))}},la={key:0},oa={key:1},sa={key:2},ia={key:3},ua={__name:"StateDisplay",props:["row"],setup(t){const a=t;return w(a.row.state),console.log(a.row.devicetype),(l,s)=>a.row.devicetype=="Switch"?(E(),P("div",la,[N(Vt,{state:a.row.state,id:a.row.id},null,8,["state","id"])])):a.row.devicetype=="Light"?(E(),P("div",oa,[N(ra,{state:a.row.state,id:a.row.id,brightness:a.row.brightness},null,8,["state","id","brightness"])])):a.row.devicetype=="Temperature"?(E(),P("div",sa,re(a.row.temp)+"\xB0/ "+re(a.row.humidity)+"% ",1)):(E(),P("div",ia,re(a.row.state),1))}},ca={class:"q-pa-md"},ba={__name:"DevicesPage",setup(t){const a=w([]);Be();const l=[{name:"Name",label:"Name",field:"name",align:"left",sortable:!0},{name:"Ident",label:"Ident",field:"ident",align:"left",sortable:!0},{name:"Unit",label:"Unit",field:"unit",align:"left",sortable:!1},{name:"Room",label:"Room",field:"room_name",align:"left",sortable:!0},{name:"action",label:"Action",field:"action"}],s={rowsPerPage:10};return Pt("api/devices/",a),(e,r)=>(E(),Le(Et,{padding:""},{default:le(()=>[Y("div",ca,[N(At,{title:"Devices",rows:a.value,columns:l,"row-key":"id",pagination:s},{"body-cell-action":le(i=>[N(It,{props:i},{default:le(()=>[N(ua,{row:i.row},null,8,["row"])]),_:2},1032,["props"])]),_:1},8,["rows"])])]),_:1}))}};export{ba as default};
