/* Allan's Handbook of Algorithms — self-contained SVG problem visualizations. */
(() => {
  "use strict";

  const NS = "http://www.w3.org/2000/svg";
  const INK = "#334650";
  const MUTED = "#77878c";
  const GREEN = "#6ba78e";
  const GREEN_PALE = "#e4f2e9";
  const BLUE = "#699cba";
  const BLUE_PALE = "#eaf3f8";
  const ORANGE = "#d68c67";
  const ORANGE_PALE = "#fbeee2";
  const YELLOW = "#e9ba68";
  const DARK = "#476b5e";
  const GRID = "#d9e3e1";
  const WHITE = "#fff";

  function el(name, attrs = {}, label = null) {
    const node = document.createElementNS(NS, name);
    for (const [key, value] of Object.entries(attrs)) {
      node.setAttribute(key, String(value));
    }
    if (label != null) node.textContent = String(label);
    return node;
  }
  function add(svg, name, attrs, value) {
    const node = el(name, attrs, value);
    svg.appendChild(node);
    return node;
  }
  function text(svg, x, y, label, size = 15, color = INK, weight = 500, extra = {}) {
    return add(svg, "text", {
      x, y, fill: color, "font-size": size,
      "font-family": "Inter, system-ui, -apple-system, sans-serif",
      "font-weight": weight, "text-anchor": "middle",
      "dominant-baseline": "middle", ...extra
    }, label);
  }
  function rect(svg, x, y, w, h, fill = WHITE, stroke = GRID, r = 10, sw = 1.5) {
    return add(svg, "rect", {x, y, width: w, height: h, rx: r, fill, stroke, "stroke-width": sw});
  }
  function line(svg, x1, y1, x2, y2, color = GRID, w = 2, dashed = false) {
    return add(svg, "line", {x1, y1, x2, y2, stroke: color, "stroke-width": w,
      "stroke-linecap": "round", ...(dashed ? {"stroke-dasharray": "6 6"} : {})});
  }
  function circle(svg, x, y, r, fill = WHITE, stroke = INK, w = 2) {
    return add(svg, "circle", {cx:x,cy:y,r,fill,stroke,"stroke-width":w});
  }
  function badge(svg,x,y,value,fill=WHITE,color=INK,w=65) {
    rect(svg,x-w/2,y-14,w,28,fill,fill==="white"?GRID:fill,8,1);
    text(svg,x,y+1,value,13,color,750);
  }
  function node(svg, x, y, label, fill = WHITE, stroke = INK, r = 25, colour = INK) {
    circle(svg,x,y,r,fill,stroke,2.5);
    text(svg,x,y+1,label,17,colour,760);
  }
  function link(svg,a,b,opt={}) {
    const r = opt.radius || 29;
    const dx=b[0]-a[0],dy=b[1]-a[1],d=Math.hypot(dx,dy)||1;
    const ux=dx/d,uy=dy/d;
    const x1=a[0]+ux*r,y1=a[1]+uy*r,x2=b[0]-ux*(r+4),y2=b[1]-uy*(r+4);
    const c=opt.color||GRID,w=opt.width||3;
    line(svg,x1,y1,x2,y2,c,w,!!opt.dash);
    if(opt.arrow){
      const size=9, px=-uy,py=ux;
      add(svg,"polygon",{points:[
        [x2,y2],[x2-ux*size+px*size*.6,y2-uy*size+py*size*.6],
        [x2-ux*size-px*size*.6,y2-uy*size-py*size*.6]
      ].map(p=>p.join(",")).join(" "),fill:c});
    }
    if(opt.weight!=null){
      const ox=-uy*(opt.side||15),oy=ux*(opt.side||15);
      const mx=(x1+x2)/2+ox,my=(y1+y2)/2+oy;
      circle(svg,mx,my,13,WHITE,GRID,1);
      text(svg,mx,my+1,opt.weight,12,INK,740);
    }
  }
  function base(svg) {
    svg.replaceChildren();
    rect(svg,1,1,718,334,"#fbfcfa","#edf1ed",14,1);
  }
  function small(svg,x,y,str){text(svg,x,y,str,12,MUTED,720,{"letter-spacing":".05em"});}

  const scenarios = {
    merge: {
      title: ["Merging overlapping intervals","Объединение пересекающихся отрезков"],
      steps: [
        ["Sort the intervals by their starting points.","Сортируем отрезки по левым концам."],
        ["Start the result with [1, 4].","Начинаем ответ с отрезка [1, 4]."],
        ["[4, 5] touches the last interval; extend it to [1, 5].","[4, 5] соприкасается с последним отрезком: расширяем его до [1, 5]."],
        ["[8, 10] does not overlap, so start another interval.","[8, 10] не пересекается с предыдущим: добавляем новый отрезок."],
        ["[9, 12] overlaps [8, 10]. The final result has two intervals.","[9, 12] пересекается с [8, 10]. В ответе остаются два отрезка."]
      ],
      draw(svg,s,ru){
        base(svg);
        const arr=[[1,4],[4,5],[8,10],[9,12]];
        const scale=v=>130+(v-1)*38.2;
        small(svg,73,52,ru?"ИСХОДНЫЕ":"INPUT");
        for(const v of [1,4,8,12]) {line(svg,scale(v),56,scale(v),243,"#e9efeb",1,true);text(svg,scale(v),43,v,12,MUTED,600);}
        arr.forEach(([a,b],i)=>{
          const y=83+i*42; const active=i===s-1;
          line(svg,scale(a),y,scale(b),y,active?ORANGE:BLUE,9);
          circle(svg,scale(a),y,5,active?ORANGE:BLUE,WHITE,1);
          circle(svg,scale(b),y,5,active?ORANGE:BLUE,WHITE,1);
          text(svg,65,y,[a,b].join("–"),13,active?ORANGE:INK,active?760:590);
        });
        line(svg,35,252,685,252,GRID,1.6);
        small(svg,77,284,ru?"ОТВЕТ":"MERGED");
        const states=[[],[[1,4]],[[1,5]],[[1,5],[8,10]],[[1,5],[8,12]]];
        states[s].forEach(([a,b],i)=>{
          const y=275+i*34;
          line(svg,scale(a),y,scale(b),y,GREEN,10);
          circle(svg,scale(a),y,5,GREEN,WHITE,1);
          circle(svg,scale(b),y,5,GREEN,WHITE,1);
          text(svg,(scale(a)+scale(b))/2,y-13,"["+a+", "+b+"]",12,DARK,730);
        });
        if(s===0)text(svg,365,287,ru?"Пока пусто":"Empty",14,MUTED,500);
      }
    },
    jump: {
      title: ["The farthest reachable position","Самая далёкая достижимая позиция"],
      steps: [
        ["Initially only index 0 is known to be reachable.","Изначально достижима только позиция 0."],
        ["From index 0 we can reach positions 1 and 2; farthest = 2.","Из позиции 0 достигаем индексов 1 и 2; farthest = 2."],
        ["Index 1 is reachable. Its jump of 3 extends farthest to 4.","Индекс 1 достижим. Прыжок длины 3 расширяет границу до индекса 4."],
        ["The last position lies within the reachable prefix. Answer: True.","Последняя позиция попала в достижимый префикс. Ответ: True."]
      ],
      draw(svg,s,ru){
        base(svg);
        const nums=[2,3,1,1,4], farthest=[0,2,4,4][s],current=[-1,0,1,-1][s];
        small(svg,360,65,ru?"ПРЫЖКИ ИЗ КАЖДОЙ КЛЕТКИ":"MAXIMUM JUMP FROM EACH CELL");
        nums.forEach((n,i)=>{
          const x=57+i*125,reachable=i<=farthest,active=i===current;
          rect(svg,x,112,110,104,active?ORANGE_PALE:reachable?GREEN_PALE:"#f3f6f5",active?ORANGE:reachable?GREEN:GRID,12,active?3:1.6);
          text(svg,x+55,155,n,31,active?"#a95e38":reachable?DARK:MUTED,780);
          text(svg,x+55,195,"i = "+i,12,MUTED,620);
        });
        line(svg,70,244,650,244,GRID,2);
        const boundary=57+farthest*125+55;
        line(svg,70,244,boundary,244,GREEN,7);
        circle(svg,boundary,244,7,GREEN,WHITE,2);
        badge(svg,Math.min(boundary,620),280,"farthest = "+farthest,GREEN_PALE,DARK,136);
        if(current>=0){
          const x=112+current*125;badge(svg,x,77,ru?"Текущий":"Current",ORANGE_PALE,"#9b6141",86);
        }
      }
    },
    oranges: {
      title: ["Multi-source breadth-first search","Поиск в ширину из нескольких источников"],
      steps: [
        ["Minute 0: the initial rotten orange is the BFS source.","Минута 0: исходный гнилой апельсин — источник BFS."],
        ["Minute 1: both adjacent fresh oranges become rotten.","Минута 1: заражаются оба соседних свежих апельсина."],
        ["Minute 2: the next BFS layer becomes rotten.","Минута 2: заражается следующий слой BFS."],
        ["Minute 3: the infection reaches the bottom row.","Минута 3: заражение достигает нижнего ряда."],
        ["Minute 4: the last orange becomes rotten. Total time: 4.","Минута 4: заражается последний апельсин. Ответ: 4."]
      ],
      draw(svg,s,ru){
        base(svg);
        const grid=[[2,1,1],[1,1,0],[0,1,1]];
        const times=[[0,1,2],[1,2,-1],[-1,3,4]];
        badge(svg,105,115,(ru?"Минута ":"Minute ")+s,BLUE_PALE,"#3e738f",145);
        let fresh=0;
        grid.forEach((row,r)=>row.forEach((cell,c)=>{
          const x=211+c*97,y=31+r*96;
          const t=times[r][c],rotten=cell===2||t>=0&&t<=s;
          if(cell===1&&t>s)fresh++;
          rect(svg,x,y,81,81,cell===0?"#eff2f0":rotten?"#f8e0dc":"#e6f2e8",cell===0?"#e2e9e4":rotten?"#e3aaa0":"#b0d4bb",12,2);
          if(cell!==0){
            circle(svg,x+40,y+42,23,rotten?"#db8574":"#84ba8f",rotten?"#bb675d":"#649d70",2);
            add(svg,"path",{d:"M "+(x+40)+" "+(y+17)+" q 4 -11 13 -7",fill:"none",stroke:"#4f8566","stroke-width":3,"stroke-linecap":"round"});
            if(rotten){
              circle(svg,x+32,y+39,2.2,"#813f38","none",0);
              circle(svg,x+49,y+39,2.2,"#813f38","none",0);
              line(svg,x+34,y+52,x+47,y+52,"#813f38",2);
            }else{
              circle(svg,x+32,y+40,2.1,"#46634d","none",0);
              circle(svg,x+49,y+40,2.1,"#46634d","none",0);
            }
          }
          if(t===s&&s>0)circle(svg,x+69,y+14,7,ORANGE,WHITE,1.5);
        }));
        badge(svg,598,202,(ru?"Свежих: ":"Fresh: ")+fresh,fresh?"#f2f6ec":GREEN_PALE,fresh?MUTED:DARK,122);
        small(svg,597,237,ru?"ПОСЛЕ ЭТОГО ШАГА":"AFTER THIS STEP");
      }
    },
    courses: {
      title: ["Kahn's topological sorting algorithm","Алгоритм Кана: топологическая сортировка"],
      steps: [
        ["Initially only course 0 has indegree 0.","Сначала только у курса 0 входящая степень равна нулю."],
        ["Remove 0; courses 1 and 2 are now available.","Удаляем 0: курсы 1 и 2 теперь доступны."],
        ["Remove 1; course 3 still depends on course 2.","Удаляем 1: курс 3 всё ещё зависит от курса 2."],
        ["Remove 2; course 3 now has indegree 0.","Удаляем 2: входящая степень курса 3 стала нулевой."],
        ["Remove 3; all four courses have been scheduled.","Удаляем 3: все четыре курса пройдены."]
      ],
      draw(svg,s,ru){
        base(svg);
        const pos=[[125,162],[334,92],[334,228],[566,162]];
        const ed=[[0,1],[0,2],[1,3],[2,3]];
        const processed=[[ ],[0],[0,1],[0,1,2],[0,1,2,3]][s];
        const indeg=[[0,1,1,2],[0,0,0,2],[0,0,0,1],[0,0,0,0],[0,0,0,0]][s];
        const queue=[[0],[1,2],[2],[3],[]][s];
        ed.forEach(([u,v])=>link(svg,pos[u],pos[v],{arrow:true,color:processed.includes(u)?GREEN:"#bdcdd0",width:3,radius:29}));
        pos.forEach(([x,y],i)=>{
          const finished=processed.includes(i),available=queue.includes(i);
          node(svg,x,y,String(i),finished?GREEN_PALE:available?ORANGE_PALE:WHITE,finished?GREEN:available?ORANGE:GRID,27);
          text(svg,x,y+46,finished?(ru?"готово":"done"):"in = "+indeg[i],12,finished?DARK:MUTED,650);
        });
        line(svg,30,288,690,288,GRID,1.5);
        small(svg,100,309,ru?"ОЧЕРЕДЬ":"QUEUE");
        if(queue.length===0)text(svg,340,309,ru?"пуста":"empty",14,MUTED);
        queue.forEach((v,i)=>badge(svg,255+i*65,309,String(v),ORANGE_PALE,"#975f3f",43));
      }
    },
    coins: {
      title: ["Building the DP array","Заполнение массива динамического программирования"],
      steps: [
        ["dp[0] = 0: no coins are needed for amount 0.","dp[0] = 0: для суммы 0 монеты не нужны."],
        ["dp[1] = 1: take a coin of value 1.","dp[1] = 1: берём монету номинала 1."],
        ["dp[2] = 2: use two coins of value 1.","dp[2] = 2: нужны две монеты по 1."],
        ["dp[3] = 1: one coin of value 3 is better.","dp[3] = 1: достаточно одной монеты номинала 3."],
        ["dp[4] = 1: choose a coin of value 4.","dp[4] = 1: выбираем монету номинала 4."],
        ["dp[5] = 2: combine coins 4 and 1.","dp[5] = 2: используем монеты 4 и 1."],
        ["dp[6] = 2: 3 + 3 beats the greedy choice 4 + 1 + 1.","dp[6] = 2: вариант 3 + 3 лучше жадного 4 + 1 + 1."]
      ],
      draw(svg,s,ru){
        base(svg);
        const dp=[0,1,2,1,1,2,2];
        small(svg,360,52,ru?"МИНИМАЛЬНОЕ ЧИСЛО МОНЕТ":"MINIMUM NUMBER OF COINS");
        dp.forEach((d,i)=>{
          const x=45+i*92,known=i<=s,active=i===s;
          rect(svg,x,95,79,103,active?ORANGE_PALE:known?GREEN_PALE:"#f5f7f6",active?ORANGE:known?GREEN:GRID,11,active?3:1.5);
          text(svg,x+39,117,"x = "+i,13,MUTED,650);
          text(svg,x+39,159,known?d:"—",30,known?INK:"#aab4b0",760);
        });
        small(svg,355,231,ru?"НОМИНАЛЫ: 1, 3, 4":"DENOMINATIONS: 1, 3, 4");
        const ways=["∅","1","1 + 1","3","4","4 + 1","3 + 3"];
        badge(svg,355,281,(ru?"Размен: ":"Coins: ")+ways[s],BLUE_PALE,"#416e88",215);
      }
    },
    matching: {
      title: ["Augmenting paths and reassignment","Увеличивающие пути и переназначение"],
      steps: [
        ["Start with no assignments. Edges show the allowed pairs.","Сначала назначений нет. Линии показывают допустимые пары."],
        ["Assign applicant A to job 0.","Назначаем кандидата A на вакансию 0."],
        ["To place B at job 0, move A from job 0 to job 1.","Чтобы назначить B на вакансию 0, переводим A с вакансии 0 на вакансию 1."],
        ["Assign C to job 2. The maximum matching has size 3.","Назначаем C на вакансию 2. Размер максимального паросочетания равен 3."]
      ],
      draw(svg,s,ru){
        base(svg);
        const left=[[156,97],[156,182],[156,267]],right=[[542,110],[542,199],[542,282]];
        const pairs=[[0,0],[0,1],[1,0],[2,1],[2,2]];
        const matches=[[],[[0,0]],[[0,1],[1,0]],[[0,1],[1,0],[2,2]]][s];
        small(svg,157,38,ru?"КАНДИДАТЫ":"APPLICANTS");small(svg,548,38,ru?"ВАКАНСИИ":"JOBS");
        const isMatched=(a,b)=>matches.some(([x,y])=>x===a&&y===b);
        pairs.forEach(([a,b])=>{
          const c=isMatched(a,b)?GREEN:s>=2&&a===0&&b===0?"#e2aaa1":"#d7e1de";
          line(svg,left[a][0]+27,left[a][1],right[b][0]-27,right[b][1],c,isMatched(a,b)?5.5:2.3,s>=2&&a===0&&b===0);
        });
        left.forEach(([x,y],i)=>node(svg,x,y,"ABC"[i],matches.some(q=>q[0]===i)?GREEN_PALE:WHITE,matches.some(q=>q[0]===i)?GREEN:GRID,27));
        right.forEach(([x,y],i)=>node(svg,x,y,i,matches.some(q=>q[1]===i)?GREEN_PALE:WHITE,matches.some(q=>q[1]===i)?GREEN:GRID,27));
        badge(svg,347,304,(ru?"Назначено: ":"Matched: ")+matches.length,GREEN_PALE,DARK,130);
      }
    },
    delay: {
      title: ["Dijkstra's shortest-path distances","Кратчайшие расстояния: алгоритм Дейкстры"],
      steps: [
        ["Initialize the source (2) with distance 0; others are infinite.","Расстояние до истока (2) равно 0, до остальных — бесконечность."],
        ["Process node 2. Distances to 1 and 3 become 1.","Обрабатываем вершину 2. Расстояния до 1 и 3 становятся равными 1."],
        ["Process node 1. No distance improves.","Обрабатываем вершину 1. Улучшений нет."],
        ["Process node 3. Relax the edge 3 → 4; d[4] = 2.","Обрабатываем вершину 3. Релаксация 3 → 4 даёт d[4] = 2."],
        ["Process node 4. The maximum distance is 2.","Обрабатываем вершину 4. Максимальное расстояние равно 2."]
      ],
      draw(svg,s,ru){
        base(svg);
        const pos={2:[117,166],1:[346,83],3:[346,241],4:[586,241]};
        const ed=[[2,1,1],[2,3,1],[3,4,1]];
        const known=[{2:0},{2:0,1:1,3:1},{2:0,1:1,3:1},{2:0,1:1,3:1,4:2},{2:0,1:1,3:1,4:2}][s];
        const fixed=[[],[2],[2,1],[2,1,3],[2,1,3,4]][s],current=[2,2,1,3,4][s];
        ed.forEach(([a,b,w])=>link(svg,pos[a],pos[b],{arrow:true,weight:w,radius:29,color:fixed.includes(a)?GREEN:"#beced0",width:3}));
        Object.entries(pos).forEach(([label,[x,y]])=>{
          const k=Number(label),done=fixed.includes(k),discovered=k in known;
          node(svg,x,y,label,done?GREEN_PALE:k===current?ORANGE_PALE:discovered?BLUE_PALE:WHITE,done?GREEN:k===current?ORANGE:GRID,29);
          badge(svg,x,y+50,"d = "+(discovered?known[k]:"∞"),done?GREEN_PALE:WHITE,done?DARK:INK,78);
        });
        small(svg,357,303,ru?"ИСТОК: ВЕРШИНА 2":"SOURCE: NODE 2");
      }
    },
    points: {
      title: ["Prim's minimum spanning tree","Минимальный остов: алгоритм Прима"],
      steps: [
        ["Start the tree at P0. No edge has been chosen.","Начинаем строить остов из точки P0. Рёбер пока нет."],
        ["Connect P1 to P0 with cost 4.","Соединяем P1 с P0, стоимость 4."],
        ["Connect P3 to P1 with cost 3.","Добавляем P3 через P1, стоимость 3."],
        ["Connect P4 to P3 with cost 4.","Добавляем P4 через P3, стоимость 4."],
        ["Connect P2 to P1 with cost 9. Total MST cost: 20.","Добавляем P2 через P1, стоимость 9. Стоимость остова: 20."]
      ],
      draw(svg,s,ru){
        base(svg);
        const P=[[101,253],[240,217],[314,64],[449,217],[591,253]];
        const chosen=[[0,1,4],[1,3,3],[3,4,4],[1,2,9]];
        const cost=[0,4,7,11,20][s];
        small(svg,350,29,ru?"МАНХЭТТЕНСКОЕ РАССТОЯНИЕ":"MANHATTAN DISTANCE");
        line(svg,78,282,650,282,GRID,1.5);
        for(let i=0;i<s;i++){const [a,b,w]=chosen[i];link(svg,P[a],P[b],{color:GREEN,width:5,weight:w,radius:23,side:-16});}
        P.forEach(([x,y],i)=>{
          const added=(i===0)||chosen.slice(0,s).some(([a,b])=>b===i);
          node(svg,x,y,"P"+i,added?GREEN_PALE:WHITE,added?GREEN:GRID,23,added?DARK:INK);
        });
        badge(svg,360,310,(ru?"Стоимость: ":"Total cost: ")+cost,GREEN_PALE,DARK,153);
      }
    },
    robber: {
      title: ["Take or skip each house","Выбрать дом или пропустить"],
      steps: [
        ["Before considering any house, the optimum is 0.","До рассмотрения первого дома оптимум равен 0."],
        ["For the first house, take 2.","Для первого дома оптимум равен 2."],
        ["For the first two houses, take 7 rather than 2.","Для первых двух домов лучше взять 7, а не 2."],
        ["Including house 2 gives 2 + 9 = 11.","Если взять дом 2, получим 2 + 9 = 11."],
        ["House 3 would not improve the optimum: it remains 11.","Дом 3 не улучшает оптимум: он остаётся равным 11."],
        ["Take house 4 as well: 2 + 9 + 1 = 12.","Можно добавить дом 4: 2 + 9 + 1 = 12."]
      ],
      draw(svg,s,ru){
        base(svg);
        const values=[2,7,9,3,1],best=[0,2,7,11,11,12][s];
        const sets=[[],[0],[1],[0,2],[0,2],[0,2,4]][s];
        small(svg,359,56,ru?"НЕ ВЫБИРАТЬ СОСЕДНИЕ ДОМА":"NO TWO ADJACENT HOUSES");
        values.forEach((v,i)=>{
          const x=51+i*129,selected=sets.includes(i),examined=i<s,active=i===s-1;
          rect(svg,x,119,107,100,selected?GREEN_PALE:examined?"#f2f5f3":WHITE,active?ORANGE:selected?GREEN:GRID,8,active?2.7:1.6);
          add(svg,"path",{d:"M "+(x+8)+" 119 L "+(x+53)+" 80 L "+(x+99)+" 119 Z",fill:selected?GREEN_PALE:"#eef2f0",stroke:active?ORANGE:selected?GREEN:GRID,"stroke-width":2,"stroke-linejoin":"round"});
          text(svg,x+53,155,"$"+v,25,selected?DARK:INK,760);
          text(svg,x+53,196,"i = "+i,12,MUTED,610);
        });
        badge(svg,359,276,(ru?"Максимум: ":"Optimal: ")+best,GREEN_PALE,DARK,148);
      }
    },
    bipartition: {
      title: ["Two-colouring the graph","Раскраска графа в два цвета"],
      steps: [
        ["Start with an uncoloured graph of dislikes.","Начинаем с нераскрашенного графа несовместимости."],
        ["Colour vertex 1 blue.","Красим вершину 1 синим."],
        ["Its neighbors 2 and 3 must be orange.","Его соседи 2 и 3 должны быть оранжевыми."],
        ["Neighbour 4 of vertex 2 must be blue. No conflicts remain.","Сосед вершины 2 — вершина 4 — должен быть синим. Противоречий нет."]
      ],
      draw(svg,s,ru){
        base(svg);
        const pos={1:[144,160],2:[342,81],3:[342,240],4:[565,81]};
        const edges=[[1,2],[1,3],[2,4]],colors=[
          {},{1:0},{1:0,2:1,3:1},{1:0,2:1,3:1,4:0}
        ][s];
        edges.forEach(([a,b])=>link(svg,pos[a],pos[b],{color:GRID,width:3,radius:29}));
        Object.entries(pos).forEach(([key,[x,y]])=>{
          const c=colors[key],fill=c==null?WHITE:c===0?BLUE_PALE:ORANGE_PALE;
          const stroke=c==null?GRID:c===0?BLUE:ORANGE;
          node(svg,x,y,key,fill,stroke,28);
        });
        line(svg,38,288,682,288,GRID,1.2);
        circle(svg,221,312,9,BLUE_PALE,BLUE,2);
        text(svg,323,312,(ru?"Группа 1: ":"Group 1: ")+(s>=1?"1"+(s===3?", 4":""):"—"),12,INK,650);
        circle(svg,451,312,9,ORANGE_PALE,ORANGE,2);
        text(svg,561,312,(ru?"Группа 2: ":"Group 2: ")+(s>=2?"2, 3":"—"),12,INK,650);
      }
    }
  };

  function create(id, isRu) {
    const scene = scenarios[id];
    if (!scene) return null;
    let step = 0;
    const title = scene.title[isRu?1:0];

    const section = document.createElement("section");
    section.className = "visual-walkthrough";
    section.setAttribute("aria-label", title);

    const heading = document.createElement("div");
    heading.className = "visual-header";
    const left = document.createElement("div");
    const kicker = document.createElement("div");
    kicker.className = "visual-kicker";
    kicker.textContent = isRu ? "ВИЗУАЛИЗАЦИЯ" : "VISUAL WALKTHROUGH";
    const name = document.createElement("h4");
    name.className = "visual-title";
    name.textContent = title;
    left.append(kicker,name);
    heading.appendChild(left);
    section.appendChild(heading);

    const stage = document.createElement("div");
    stage.className = "visual-stage";
    const svg = el("svg", {viewBox:"0 0 720 336",preserveAspectRatio:"xMidYMid meet",role:"img","aria-label":title});
    svg.classList.add("visual-svg");
    stage.appendChild(svg);
    section.appendChild(stage);

    const caption = document.createElement("p");
    caption.className = "visual-caption";
    caption.setAttribute("aria-live","polite");
    caption.setAttribute("aria-atomic","true");
    section.appendChild(caption);

    const toolbar = document.createElement("div");
    toolbar.className = "visual-toolbar";
    const buttons = document.createElement("div");
    buttons.className = "visual-buttons";
    const prev = document.createElement("button");
    prev.type="button";prev.className="visual-prev";
    prev.textContent=isRu?"← Назад":"← Previous";
    const next = document.createElement("button");
    next.type="button";next.className="visual-next";
    const reset = document.createElement("button");
    reset.type="button";reset.className="visual-reset";
    reset.textContent=isRu?"Сначала":"Reset";
    buttons.append(prev,next,reset);
    toolbar.appendChild(buttons);
    const counter = document.createElement("span");
    counter.className="visual-counter";
    toolbar.appendChild(counter);
    section.appendChild(toolbar);

    function render(){
      scene.draw(svg,step,isRu);
      caption.textContent=scene.steps[step][isRu?1:0];
      counter.textContent=(step+1)+" / "+scene.steps.length;
      prev.disabled=step===0;
      next.disabled=step===scene.steps.length-1;
      next.textContent=(isRu?"Далее":"Next")+" →";
      reset.disabled=step===0;
    }
    prev.addEventListener("click",()=>{if(step>0){step--;render();}});
    next.addEventListener("click",()=>{if(step<scene.steps.length-1){step++;render();}});
    reset.addEventListener("click",()=>{step=0;render();});
    render();
    return section;
  }

  window.AHAVisuals = {create};
})();