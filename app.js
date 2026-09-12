
const DEFAULTS = {
  insertion: [7,3,8,2,6,4,9,1],
  merge: [8,3,6,2,7,1,5,4],
  quick: [6,2,9,4,7,1,8,3]
};

function randomArray() {
  const pool = [1,2,3,4,5,6,7,8,9];
  for (let i=pool.length-1;i>0;i--) {
    const j=Math.floor(Math.random()*(i+1));
    [pool[i],pool[j]]=[pool[j],pool[i]];
  }
  return pool.slice(0,8);
}

function insertionSteps(input) {
  const a=[...input], steps=[{array:[...a], active:[], fixed:[0], text:"The first element is a sorted prefix of length 1."}];
  for(let i=1;i<a.length;i++){
    const key=a[i]; let j=i-1;
    steps.push({array:[...a],active:[i],fixed:[...Array(i).keys()],text:`Take ${key} as the next key.`});
    while(j>=0 && a[j]>key){
      a[j+1]=a[j];
      steps.push({array:[...a],active:[j,j+1],fixed:[...Array(j).keys()],text:`${a[j]} is larger than ${key}, so shift it one position right.`});
      j--;
    }
    a[j+1]=key;
    steps.push({array:[...a],active:[j+1],fixed:[...Array(i+1).keys()],text:`Insert ${key}. The sorted prefix now has length ${i+1}.`});
  }
  steps.push({array:[...a],active:[],fixed:[...Array(a.length).keys()],text:"Done. The entire array is sorted."});
  return steps;
}

function mergeSteps(input) {
  const a=[...input], steps=[{array:[...a],active:[],fixed:[],text:"We recursively sort smaller ranges, then merge them."}];
  const aux=new Array(a.length);
  function sort(l,r){
    if(r-l<=1) return;
    const m=Math.floor((l+r)/2);
    sort(l,m); sort(m,r);
    let i=l,j=m,k=l;
    steps.push({array:[...a],active:[...Array(r-l).keys()].map(x=>x+l),fixed:[],text:`Merge the sorted ranges [${l}, ${m}) and [${m}, ${r}).`});
    while(i<m && j<r){
      if(a[i]<=a[j]) aux[k++]=a[i++];
      else aux[k++]=a[j++];
    }
    while(i<m) aux[k++]=a[i++];
    while(j<r) aux[k++]=a[j++];
    for(k=l;k<r;k++) a[k]=aux[k];
    steps.push({array:[...a],active:[...Array(r-l).keys()].map(x=>x+l),fixed:[],text:`Merged range [${l}, ${r}) is now sorted.`});
  }
  sort(0,a.length);
  steps.push({array:[...a],active:[],fixed:[...Array(a.length).keys()],text:"Done. All merge levels are complete."});
  return steps;
}

function quickSteps(input) {
  const a=[...input], steps=[{array:[...a],active:[],fixed:[],text:"Partition around pivots until every subarray is trivial."}];
  function partition(lo,hi){
    const pivot=a[hi];
    steps.push({array:[...a],active:[...Array(hi-lo+1).keys()].map(x=>x+lo),pivot:[hi],fixed:[],text:`Use ${pivot} as pivot for positions ${lo}…${hi}.`});
    let i=lo;
    for(let j=lo;j<hi;j++){
      if(a[j]<pivot){
        [a[i],a[j]]=[a[j],a[i]];
        steps.push({array:[...a],active:[i,j],pivot:[hi],fixed:[],text:`${a[i]} belongs left of pivot ${pivot}.`});
        i++;
      }
    }
    [a[i],a[hi]]=[a[hi],a[i]];
    steps.push({array:[...a],active:[i],pivot:[i],fixed:[i],text:`Pivot ${pivot} is now in its final position ${i}.`});
    return i;
  }
  function sort(lo,hi){
    if(lo>=hi) return;
    const p=partition(lo,hi);
    sort(lo,p-1); sort(p+1,hi);
  }
  sort(0,a.length-1);
  steps.push({array:[...a],active:[],fixed:[...Array(a.length).keys()],text:"Done. Every pivot ended in its final position."});
  return steps;
}

function buildSteps(type, array){
  if(type==="insertion") return insertionSteps(array);
  if(type==="merge") return mergeSteps(array);
  return quickSteps(array);
}

function render(viz){
  const bars=viz.querySelector(".bars");
  const caption=viz.querySelector(".step-caption");
  const step=viz._steps[viz._index];
  bars.innerHTML="";
  step.array.forEach((value,idx)=>{
    const el=document.createElement("div");
    el.className="bar";
    el.style.setProperty("--value", value);
    el.textContent=value;
    if((step.active||[]).includes(idx)) el.classList.add("active");
    if((step.fixed||[]).includes(idx)) el.classList.add("fixed");
    if((step.pivot||[]).includes(idx)) el.classList.add("pivot");
    bars.appendChild(el);
  });
  caption.textContent=step.text;
}

function initVisualizer(viz){
  const type=viz.dataset.algorithm;
  viz._array=[...DEFAULTS[type]];
  viz._steps=buildSteps(type,viz._array);
  viz._index=0;
  render(viz);

  viz.querySelector('[data-action="next"]').addEventListener("click",()=>{
    viz._index=Math.min(viz._index+1,viz._steps.length-1);
    render(viz);
  });
  viz.querySelector('[data-action="reset"]').addEventListener("click",()=>{
    viz._array=[...DEFAULTS[type]];
    viz._steps=buildSteps(type,viz._array);
    viz._index=0;
    render(viz);
  });
  viz.querySelector('[data-action="randomize"]').addEventListener("click",()=>{
    viz._array=randomArray();
    viz._steps=buildSteps(type,viz._array);
    viz._index=0;
    render(viz);
  });
}

document.addEventListener("DOMContentLoaded",()=>{
  document.querySelectorAll(".visualizer").forEach(initVisualizer);

  document.querySelectorAll(".reveal").forEach(btn=>{
    btn.addEventListener("click",()=>{
      const box=document.getElementById(btn.dataset.target);
      box.classList.toggle("show");
      btn.textContent=box.classList.contains("show") ? "Hide answer" : "Show answer";
    });
  });

  const links=[...document.querySelectorAll(".sidebar a")];
  const sections=links.map(a=>document.querySelector(a.getAttribute("href"))).filter(Boolean);
  const observer=new IntersectionObserver(entries=>{
    entries.forEach(entry=>{
      if(entry.isIntersecting){
        links.forEach(a=>a.style.cssText="");
        const active=links.find(a=>a.getAttribute("href")==="#"+entry.target.id);
        if(active) active.style.cssText="background:#ecefe5;color:#17202a;font-weight:750";
      }
    });
  },{rootMargin:"-25% 0px -65% 0px",threshold:0});
  sections.forEach(s=>observer.observe(s));
});
