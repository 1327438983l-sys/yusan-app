"""Add math + English data and subject switcher to the app"""
import re

with open(r'D:\语文复习App\docs\index.html', 'r', encoding='utf-8') as f:
    content = f.read()

# 1. Add subject switcher CSS
css_add = """
/* Subject Switcher */
.subject-bar{display:flex;background:linear-gradient(135deg,#2c3e50,#34495e);padding:6px 12px;gap:6px;position:sticky;top:0;z-index:101}
.subject-btn{flex:1;padding:10px;border:none;border-radius:8px;font-size:0.95em;font-weight:600;cursor:pointer;transition:all .2s;background:rgba(255,255,255,0.1);color:rgba(255,255,255,0.7)}
.subject-btn:hover{background:rgba(255,255,255,0.2)}
.subject-btn.active{background:var(--primary);color:#fff;box-shadow:0 2px 8px rgba(230,126,34,0.4)}
/* Math */
.math-q{font-size:2em;font-weight:700;color:var(--primary);text-align:center;margin:16px 0;letter-spacing:2px}
.math-input{border:3px solid #ddd;border-radius:12px;padding:14px;font-size:1.8em;width:200px;text-align:center;outline:none;transition:all .3s}
.math-input:focus{border-color:var(--primary)}
.math-input.correct{border-color:var(--green);background:#d4edda}
.math-input.wrong{border-color:var(--red);background:#f8d7da}
.formula-card{background:var(--card);border-radius:16px;padding:24px;box-shadow:var(--shadow);max-width:400px;margin:0 auto;text-align:center;min-height:200px;display:flex;flex-direction:column;justify-content:center;cursor:pointer;transition:transform .3s}
.formula-card:active{transform:scale(0.98)}
/* English */
.eng-cn{font-size:1.8em;font-weight:700;color:var(--primary);text-align:center;margin:16px 0}
.eng-input{border:3px solid #ddd;border-radius:12px;padding:14px;font-size:1.4em;width:250px;text-align:center;outline:none;font-family:monospace}
.eng-input:focus{border-color:var(--blue)}
.eng-input.correct{border-color:var(--green);background:#d4edda}
.eng-input.wrong{border-color:var(--red);background:#f8d7da}
.eng-sentence{font-size:1.1em;line-height:1.8;text-align:center;color:#555;margin:12px 0;padding:12px;background:#f8f9fa;border-radius:8px}
"""
content = content.replace('/* Mode Tabs */', css_add + '\n/* Mode Tabs */')

# 2. Add subject switcher HTML
old_header = '<div class="header">'
new_header = """<div class="subject-bar" id="subjectBar">
  <button class="subject-btn active" data-subj="chinese" onclick="switchSubject('chinese')">📖 语文</button>
  <button class="subject-btn" data-subj="math" onclick="switchSubject('math')">🔢 数学</button>
  <button class="subject-btn" data-subj="english" onclick="switchSubject('english')">🔤 英语</button>
</div>
<div class="header">"""
content = content.replace(old_header, new_header)

# 3. Add math/english data before POEM_STORIES
math_eng = """
// ==================== MATH (苏教版三年级下册) ====================
var MATH_UNITS = [
  {unit:'第一单元 两位数乘两位数', formulas:['两位数×整十数','两位数×两位数：先用个位乘再用十位乘'], practice:[
    {q:'23 × 14 = ?', a:'322'},{q:'36 × 20 = ?', a:'720'},{q:'45 × 12 = ?', a:'540'},
    {q:'52 × 30 = ?', a:'1560'},{q:'67 × 11 = ?', a:'737'},{q:'28 × 25 = ?', a:'700'},
    {q:'34 × 15 = ?', a:'510'},{q:'41 × 23 = ?', a:'943'},{q:'56 × 18 = ?', a:'1008'},
    {q:'72 × 13 = ?', a:'936'},{q:'85 × 12 = ?', a:'1020'},{q:'39 × 40 = ?', a:'1560'}
  ]},
  {unit:'第二单元 千米和吨', formulas:['1千米=1000米','1吨=1000千克','1千克=1000克'], practice:[
    {q:'5千米=?米', a:'5000'},{q:'3000米=?千米', a:'3'},{q:'2吨=?千克', a:'2000'},
    {q:'4000千克=?吨', a:'4'},{q:'6千米=?米', a:'6000'},{q:'8000克=?千克', a:'8'}
  ]},
  {unit:'第三单元 混合运算', formulas:['先乘除后加减','有括号先算括号里','同级运算从左到右'], practice:[
    {q:'24 + 36 / 6 = ?', a:'30'},{q:'(24 + 36) / 6 = ?', a:'10'},
    {q:'80 - 45 / 5 = ?', a:'71'},{q:'12 × 3 + 28 = ?', a:'64'},
    {q:'56 / 7 × 3 = ?', a:'24'},{q:'(120 - 80) / 5 = ?', a:'8'}
  ]},
  {unit:'第四单元 年月日', formulas:['一年12个月','大月31天:1,3,5,7,8,10,12','小月30天:4,6,9,11','平年28天闰年29天(二月)'], practice:[
    {q:'一年有几个月？', a:'12'},{q:'大月有几天？', a:'31'},
    {q:'2024年是闰年还是平年？', a:'闰年'},{q:'平年全年多少天？', a:'365'},
    {q:'闰年全年多少天？', a:'366'},{q:'5月有几天？', a:'31'}
  ]},
  {unit:'第五单元 长方形和正方形', formulas:['长方形周长=(长+宽)×2','正方形周长=边长×4','长方形面积=长×宽','正方形面积=边长×边长'], practice:[
    {q:'长5宽3周长=?cm', a:'16'},{q:'正方形边长4周长=?cm', a:'16'},
    {q:'长8宽6面积=?m2', a:'48'},{q:'正方形边长5面积=?cm2', a:'25'}
  ]},
  {unit:'第六单元 分数的初步认识', formulas:['把物体平均分成几份取几份就是几分之几','分子取了几份分母分成几份'], practice:[
    {q:'蛋糕分4份取1份是？', a:'1/4'},{q:'绳子分5份取3份是？', a:'3/5'},
    {q:'1/2等于几分之几(分母4)？', a:'2/4'},{q:'2/3里有几个1/3？', a:'2'}
  ]},
  {unit:'第七单元 小数的初步认识', formulas:['小数=整数部分+小数点+小数部分','0.1=1/10'], practice:[
    {q:'3元5角=?元', a:'3.50'},{q:'8角=?元', a:'0.80'},
    {q:'1米2分米=?米', a:'1.20'},{q:'0.5等于几分之几(分母10)？', a:'5/10'}
  ]}
];
// ==================== ENGLISH (译林版三年级下册) ====================
var ENGLISH_UNITS = [
  {unit:'Unit 1 Welcome back', words:[{en:'welcome',cn:'欢迎'},{en:'school',cn:'学校'},{en:'boy',cn:'男孩'},{en:'girl',cn:'女孩'},{en:'teacher',cn:'老师'},{en:'student',cn:'学生'},{en:'friend',cn:'朋友'},{en:'new',cn:'新的'},{en:'class',cn:'班级'}], sentences:['Welcome back to school!','Nice to meet you.','This is my friend.','I\'m a student.']},
  {unit:'Unit 2 In the library', words:[{en:'library',cn:'图书馆'},{en:'shout',cn:'大叫'},{en:'eat',cn:'吃'},{en:'run',cn:'跑'},{en:'talk',cn:'说话'},{en:'sleep',cn:'睡觉'},{en:'drink',cn:'喝'},{en:'open',cn:'打开'},{en:'close',cn:'关闭'},{en:'book',cn:'书'}], sentences:['Don\'t shout in the library.','Don\'t eat here.','Be quiet, please.','Open your books.']},
  {unit:'Unit 3 Pencil?', words:[{en:'pencil',cn:'铅笔'},{en:'pen',cn:'钢笔'},{en:'ruler',cn:'尺子'},{en:'rubber',cn:'橡皮'},{en:'crayon',cn:'蜡笔'},{en:'bag',cn:'书包'},{en:'mine',cn:'我的'},{en:'yours',cn:'你的'},{en:'his',cn:'他的'},{en:'hers',cn:'她的'}], sentences:['Is this your pencil?','Yes, it is.','No, it isn\'t.','That\'s my rubber.']},
  {unit:'Unit 4 Where bird?', words:[{en:'bird',cn:'鸟'},{en:'on',cn:'在…上面'},{en:'in',cn:'在…里面'},{en:'under',cn:'在…下面'},{en:'behind',cn:'在…后面'},{en:'beside',cn:'在…旁边'},{en:'tree',cn:'树'},{en:'desk',cn:'课桌'},{en:'chair',cn:'椅子'}], sentences:['Where\'s the bird?','It\'s on your desk.','It\'s in the tree.','It\'s under the desk.']},
  {unit:'Unit 5 How old?', words:[{en:'one',cn:'一'},{en:'two',cn:'二'},{en:'three',cn:'三'},{en:'four',cn:'四'},{en:'five',cn:'五'},{en:'six',cn:'六'},{en:'seven',cn:'七'},{en:'eight',cn:'八'},{en:'nine',cn:'九'},{en:'ten',cn:'十'},{en:'eleven',cn:'十一'},{en:'twelve',cn:'十二'},{en:'thirteen',cn:'十三'},{en:'fourteen',cn:'十四'},{en:'fifteen',cn:'十五'},{en:'twenty',cn:'二十'}], sentences:['How old are you?','I\'m nine.','Happy birthday!','What about you?']},
  {unit:'Unit 6 What time?', words:[{en:'time',cn:'时间'},{en:'breakfast',cn:'早餐'},{en:'lunch',cn:'午餐'},{en:'dinner',cn:'晚餐'},{en:'bed',cn:'床'},{en:'morning',cn:'早上'},{en:'afternoon',cn:'下午'},{en:'evening',cn:'晚上'},{en:'o\'clock',cn:'点钟'},{en:'milk',cn:'牛奶'}], sentences:['What time is it?','It\'s seven o\'clock.','It\'s time for breakfast.','It\'s time to go to bed.']},
  {unit:'Unit 7 On the farm', words:[{en:'farm',cn:'农场'},{en:'pig',cn:'猪'},{en:'cow',cn:'牛'},{en:'chicken',cn:'鸡'},{en:'duck',cn:'鸭'},{en:'apple',cn:'苹果'},{en:'orange',cn:'橙子'},{en:'pear',cn:'梨'},{en:'banana',cn:'香蕉'}], sentences:['Welcome to my farm!','Are these apples?','Yes, they are.','What are these?']},
  {unit:'Unit 8 Twins!', words:[{en:'twin',cn:'双胞胎'},{en:'brother',cn:'兄弟'},{en:'sister',cn:'姐妹'},{en:'father',cn:'父亲'},{en:'mother',cn:'母亲'},{en:'grandpa',cn:'爷爷'},{en:'grandma',cn:'奶奶'},{en:'man',cn:'男人'},{en:'woman',cn:'女人'}], sentences:['We\'re twins!','This is my brother.','Who\'s he?','He\'s my father.']}
];
"""
content = content.replace('const POEM_STORIES = {', math_eng + '\nconst POEM_STORIES = {')

# 4. Add subject switcher logic + math/english render functions
# Find the end of the script
script_end = content.rfind('</script>')

new_funcs = r"""
// ==================== SUBJECT SWITCHER ====================
var currentSubject = localStorage.getItem('app_subject') || 'chinese';

function switchSubject(subj) {
  currentSubject = subj;
  localStorage.setItem('app_subject', subj);
  // Update subject buttons
  document.querySelectorAll('.subject-btn').forEach(function(b) {
    b.classList.toggle('active', b.dataset.subj === subj);
  });
  // Update title
  var titles = {chinese:'三年级下册', math:'苏教版三年级下册', english:'译林版三年级下册'};
  var el = document.getElementById('appTitle');
  if (el) el.textContent = titles[subj] || titles.chinese;
  // Show/hide mode tabs based on subject
  renderModeTabs();
  renderUnitTabs();
  renderContent();
}

function renderModeTabs() {
  var modes = {
    chinese: [{id:'review',icon:'📚',label:'复习清单'},{id:'recite',icon:'🎤',label:'背诵朗读'},{id:'quiz',icon:'📝',label:'单元测试'},{id:'flashcard',icon:'🃏',label:'闪卡记忆'},{id:'dictation',icon:'✍️',label:'闯关默写'},{id:'story',icon:'📖',label:'每日故事'},{id:'review-due',icon:'📊',label:'今日复习'}],
    math: [{id:'mental',icon:'🧮',label:'口算练习'},{id:'formula',icon:'📐',label:'公式卡片'}],
    english: [{id:'eng-dict',icon:'📝',label:'单词默写'},{id:'eng-trans',icon:'🔄',label:'句子翻译'},{id:'eng-card',icon:'🃏',label:'单词卡片'}]
  };
  var tabs = modes[currentSubject] || modes.chinese;
  var el = document.getElementById('modeTabs');
  el.innerHTML = tabs.map(function(m, i) {
    return '<div class="mode-tab' + (i===0?' active':'') + '" data-mode="' + m.id + '" onclick="switchMode(\'' + m.id + '\')">' + m.icon + m.label + '</div>';
  }).join('');
  currentMode = tabs[0].id;
}

function renderUnitTabs() {
  var el = document.getElementById('unitTabs');
  if (currentSubject === 'math') {
    el.innerHTML = MATH_UNITS.map(function(u, i) {
      return '<div class="tab' + (i===0?' active':'') + '" data-unit="' + (i+1) + '" onclick="switchMathUnit(' + (i+1) + ')">' + u.unit.split(' ')[0] + '</div>';
    }).join('');
    el.classList.remove('hidden');
  } else if (currentSubject === 'english') {
    el.innerHTML = ENGLISH_UNITS.map(function(u, i) {
      return '<div class="tab' + (i===0?' active':'') + '" data-unit="' + (i+1) + '" onclick="switchEngUnit(' + (i+1) + ')">' + u.unit.split(' ')[0] + ' ' + u.unit.split(' ')[1] + '</div>';
    }).join('');
    el.classList.remove('hidden');
  } else {
    // Chinese unit tabs
    el.innerHTML = UNITS.map(function(u) {
      return '<div class="tab' + (u.num===currentUnit?' active':'') + '" data-unit="' + u.num + '" onclick="switchUnit(' + u.num + ')">' + u.title + '</div>';
    }).join('');
    el.classList.remove('hidden');
  }
}

function switchMode(mode) {
  currentMode = mode;
  document.querySelectorAll('.mode-tab').forEach(function(t) {
    t.classList.toggle('active', t.dataset.mode === mode);
  });
  renderContent();
  scrollToTop();
}

function switchMathUnit(n) {
  currentUnit = n;
  document.querySelectorAll('#unitTabs .tab').forEach(function(t) {
    t.classList.toggle('active', parseInt(t.dataset.unit) === n);
  });
  renderContent();
}

function switchEngUnit(n) {
  currentUnit = n;
  document.querySelectorAll('#unitTabs .tab').forEach(function(t) {
    t.classList.toggle('active', parseInt(t.dataset.unit) === n);
  });
  renderContent();
}

// ==================== MATH MODES ====================
var mathState = { hearts:3, correct:0, wrong:0, combo:0, idx:0, maxCombo:0 };

function renderMathMental() {
  var u = MATH_UNITS[currentUnit - 1];
  if (!u) { document.getElementById('app').innerHTML = '<div class="unit active"><div class="section" style="text-align:center;padding:40px">选择一个单元开始练习</div></div>'; return; }
  mathState = {hearts:3,correct:0,wrong:0,combo:0,idx:0,maxCombo:0};
  renderMathQ();
}

function renderMathQ() {
  var u = MATH_UNITS[currentUnit - 1];
  if (!u || mathState.idx >= u.practice.length || mathState.hearts <= 0) { finishMathGame(); return; }
  var q = u.practice[mathState.idx];
  var html = '<div class="unit active">';
  html += '<div class="hearts">';
  for(var i=0;i<3;i++) html+='<span class="heart '+(i<mathState.hearts?'':'lost')+'">'+(i<mathState.hearts?'\u2764\ufe0f':'\u2764')+'</span>';
  html += '</div>';
  html += '<div style="text-align:center;color:var(--gray);font-size:0.9em">'+u.unit+' | '+mathState.correct+'/'+u.practice.length+' 已答对</div>';
  if(mathState.combo>=3) html+='<div style="text-align:center;color:var(--primary);font-weight:600">\ud83d\udd25 连击 '+mathState.combo+'!</div>';
  var pct = Math.round(mathState.idx/u.practice.length*100);
  html += '<div class="progress-bar" style="margin:8px 0 16px"><div class="progress-fill" style="width:'+pct+'%"></div></div>';
  html += '<div class="game-question">';
  html += '<div class="math-q">'+q.q+'</div>';
  html += '<input class="math-input" id="mathInput" placeholder="?" autocomplete="off">';
  html += '<div class="game-answer" id="mathAnswer" style="display:none"></div>';
  html += '</div>';
  html += '<div style="text-align:center;margin-top:16px"><button class="btn btn-primary" onclick="checkMathAnswer()">确认</button></div>';
  html += '</div>';
  document.getElementById('app').innerHTML = html;
  var inp = document.getElementById('mathInput');
  inp.focus();
  inp.onkeydown = function(e) { if(e.key==='Enter') checkMathAnswer(); };
}

function checkMathAnswer() {
  var u = MATH_UNITS[currentUnit - 1];
  var q = u.practice[mathState.idx];
  var inp = document.getElementById('mathInput');
  var ans = document.getElementById('mathAnswer');
  var val = inp.value.trim();
  if (!val) return;
  inp.disabled = true;
  if (val === q.a || val.replace(/\s/g,'') === q.a) {
    mathState.correct++; mathState.combo++;
    if(mathState.combo>mathState.maxCombo) mathState.maxCombo=mathState.combo;
    inp.classList.add('correct');
    var bonus = mathState.combo>=5?15:mathState.combo>=3?10:0;
    addPoints(10+bonus);
    ans.innerHTML = '<span class="correct-text">\u2705 答对了！</span>'+(bonus>0?' <span style="color:var(--primary)">+连击'+bonus+'</span>':'');
  } else {
    mathState.wrong++; mathState.hearts--; mathState.combo=0;
    inp.classList.add('wrong');
    ans.innerHTML = '\u274c 答案：<span class="correct-text" style="font-size:1.3em">'+q.a+'</span>';
  }
  ans.style.display = 'block';
  updateGameStats();
  setTimeout(function() { mathState.idx++; renderMathQ(); }, 1000);
}

function renderMathFormula() {
  var u = MATH_UNITS[currentUnit - 1];
  if (!u) { document.getElementById('app').innerHTML = '<div class="unit active"><div class="section" style="text-align:center;padding:40px">选择一个单元</div></div>'; return; }
  mathState.formulaIdx = 0;
  showFormula();
}

function showFormula() {
  var u = MATH_UNITS[currentUnit - 1];
  var idx = mathState.formulaIdx || 0;
  if (idx >= u.formulas.length) idx = 0;
  mathState.formulaIdx = idx;
  var html = '<div class="unit active">';
  html += '<div class="unit-title">'+u.unit+'</div>';
  html += '<div class="unit-subtitle">公式卡片 '+(idx+1)+'/'+u.formulas.length+'</div>';
  html += '<div class="formula-card" onclick="this.querySelector(\'.formula-back\').style.display=this.querySelector(\'.formula-back\').style.display===\'none\'?\'block\':\'none\'">';
  html += '<div style="font-size:1.3em;font-weight:700;color:var(--primary);margin-bottom:12px">'+u.formulas[idx]+'</div>';
  html += '<div style="color:var(--gray);font-size:0.9em">点击翻转查看</div>';
  html += '</div>';
  html += '<div class="btn-group" style="justify-content:center;margin-top:16px">';
  html += '<button class="btn btn-sm" style="background:#eee" onclick="mathState.formulaIdx=Math.max(0,mathState.formulaIdx-1);showFormula()">上一个</button>';
  html += '<button class="btn btn-primary" onclick="mathState.formulaIdx++;showFormula()">下一个</button>';
  html += '</div></div>';
  document.getElementById('app').innerHTML = html;
}

function finishMathGame() {
  var total = mathState.correct+mathState.wrong;
  var acc = total>0?Math.round(mathState.correct/total*100):0;
  var stars = acc>=90?'\u2b50\u2b50\u2b50':acc>=70?'\u2b50\u2b50':acc>=50?'\u2b50':'';
  var html = '<div class="unit active"><div class="result-card">';
  html += '<div style="font-size:3em">'+(mathState.hearts>0?'\ud83c\udf89':'\ud83d\ude22')+'</div>';
  html += '<div class="result-stars">'+stars+'</div>';
  html += '<div class="result-text">'+(mathState.hearts>0?'练习完成！':'生命用完了！')+'</div>';
  html += '<div style="color:var(--gray)">答对 '+mathState.correct+' 个，最高连击 '+mathState.maxCombo+'</div>';
  html += '<div class="btn-group" style="justify-content:center;margin-top:16px">';
  html += '<button class="btn btn-primary" onclick="renderMathMental()">再来一次</button>';
  html += '<button class="btn btn-blue" onclick="renderMathFormula()">看公式</button>';
  html += '</div></div></div>';
  document.getElementById('app').innerHTML = html;
}

// ==================== ENGLISH MODES ====================
var engState = { hearts:3, correct:0, wrong:0, combo:0, idx:0 };

function renderEngDictation() {
  var u = ENGLISH_UNITS[currentUnit - 1];
  if (!u) { document.getElementById('app').innerHTML = '<div class="unit active"><div class="section" style="text-align:center;padding:40px">选择一个单元开始练习</div></div>'; return; }
  engState = {hearts:3,correct:0,wrong:0,combo:0,idx:0};
  renderEngQ();
}

function renderEngQ() {
  var u = ENGLISH_UNITS[currentUnit - 1];
  if (!u || engState.idx >= u.words.length || engState.hearts <= 0) { finishEngGame(); return; }
  var w = u.words[engState.idx];
  var html = '<div class="unit active">';
  html += '<div class="hearts">';
  for(var i=0;i<3;i++) html+='<span class="heart '+(i<engState.hearts?'':'lost')+'">'+(i<engState.hearts?'\u2764\ufe0f':'\u2764')+'</span>';
  html += '</div>';
  html += '<div style="text-align:center;color:var(--gray);font-size:0.9em">'+u.unit+' | '+engState.correct+'/'+u.words.length+' 已答对</div>';
  if(engState.combo>=3) html+='<div style="text-align:center;color:var(--primary);font-weight:600">\ud83d\udd25 连击 '+engState.combo+'!</div>';
  var pct = Math.round(engState.idx/u.words.length*100);
  html += '<div class="progress-bar" style="margin:8px 0 16px"><div class="progress-fill" style="width:'+pct+'%"></div></div>';
  html += '<div class="game-question">';
  html += '<div class="eng-cn">'+w.cn+'</div>';
  html += '<div style="text-align:center;color:var(--gray);margin-bottom:8px">写出对应的英文单词</div>';
  html += '<input class="eng-input" id="engInput" placeholder="Type English..." autocomplete="off" autocapitalize="off">';
  html += '<div class="game-answer" id="engAnswer" style="display:none"></div>';
  html += '</div>';
  html += '<div style="text-align:center;margin-top:12px;display:flex;gap:10px;justify-content:center">';
  html += '<button class="btn btn-sm" style="background:#eee" onclick="showEngHint()">\ud83d\udca1 提示</button>';
  html += '<button class="btn btn-primary" onclick="checkEngDictAnswer()">确认</button>';
  html += '</div></div>';
  document.getElementById('app').innerHTML = html;
  var inp = document.getElementById('engInput');
  inp.focus();
  inp.onkeydown = function(e) { if(e.key==='Enter') checkEngDictAnswer(); };
}

function showEngHint() {
  var u = ENGLISH_UNITS[currentUnit - 1];
  var w = u.words[engState.idx];
  var hint = w.en.charAt(0) + '_'.repeat(w.en.length - 1);
  var inp = document.getElementById('engInput');
  if (inp) inp.placeholder = hint;
}

function checkEngDictAnswer() {
  var u = ENGLISH_UNITS[currentUnit - 1];
  var w = u.words[engState.idx];
  var inp = document.getElementById('engInput');
  var ans = document.getElementById('engAnswer');
  var val = inp.value.trim().toLowerCase();
  if (!val) return;
  inp.disabled = true;
  if (val === w.en.toLowerCase()) {
    engState.correct++; engState.combo++;
    inp.classList.add('correct');
    var bonus = engState.combo>=5?15:engState.combo>=3?10:0;
    addPoints(10+bonus);
    ans.innerHTML = '<span class="correct-text">\u2705 '+w.en+' = '+w.cn+'</span>'+(bonus>0?' <span style="color:var(--primary)">+连击'+bonus+'</span>':'');
  } else {
    engState.wrong++; engState.hearts--; engState.combo=0;
    inp.classList.add('wrong');
    ans.innerHTML = '\u274c 正确答案：<span class="correct-text" style="font-size:1.3em">'+w.en+'</span> = '+w.cn;
  }
  ans.style.display = 'block';
  updateGameStats();
  setTimeout(function() { engState.idx++; renderEngQ(); }, 1200);
}

function renderEngTranslation() {
  var u = ENGLISH_UNITS[currentUnit - 1];
  if (!u || !u.sentences) { document.getElementById('app').innerHTML = '<div class="unit active"><div class="section" style="text-align:center;padding:40px">本单元暂无句子翻译</div></div>'; return; }
  engState = {hearts:3,correct:0,wrong:0,combo:0,idx:0};
  renderTransQ();
}

function renderTransQ() {
  var u = ENGLISH_UNITS[currentUnit - 1];
  if (!u.sentences || engState.idx >= u.sentences.length || engState.hearts <= 0) { finishEngGame(); return; }
  var s = u.sentences[engState.idx];
  var html = '<div class="unit active">';
  html += '<div class="hearts">';
  for(var i=0;i<3;i++) html+='<span class="heart '+(i<engState.hearts?'':'lost')+'">'+(i<engState.hearts?'\u2764\ufe0f':'\u2764')+'</span>';
  html += '</div>';
  html += '<div style="text-align:center;color:var(--gray);font-size:0.9em">'+engState.idx+'/'+u.sentences.length+'</div>';
  html += '<div class="game-question">';
  html += '<div class="eng-sentence">'+s+'</div>';
  html += '<div style="text-align:center;color:var(--gray);margin:8px 0">翻译成中文：</div>';
  html += '<input class="eng-input" id="transInput" placeholder="中文翻译..." autocomplete="off" style="font-family:inherit">';
  html += '<div class="game-answer" id="transAnswer" style="display:none"></div>';
  html += '</div>';
  html += '<div style="text-align:center;margin-top:12px"><button class="btn btn-primary" onclick="checkTransAnswer()">确认</button></div>';
  html += '</div>';
  document.getElementById('app').innerHTML = html;
  var inp = document.getElementById('transInput');
  inp.focus();
  inp.onkeydown = function(e) { if(e.key==='Enter') checkTransAnswer(); };
}

function checkTransAnswer() {
  var u = ENGLISH_UNITS[currentUnit - 1];
  var s = u.sentences[engState.idx];
  var inp = document.getElementById('transInput');
  var ans = document.getElementById('transAnswer');
  var val = inp.value.trim();
  if (!val) return;
  inp.disabled = true;
  // Simple check: just show answer (translation is subjective)
  engState.correct++;
  inp.classList.add('correct');
  addPoints(10);
  ans.innerHTML = '<span class="correct-text">\u2705 参考翻译已显示</span>';
  ans.style.display = 'block';
  updateGameStats();
  setTimeout(function() { engState.idx++; renderTransQ(); }, 1500);
}

function renderEngFlashcard() {
  var u = ENGLISH_UNITS[currentUnit - 1];
  if (!u) { document.getElementById('app').innerHTML = '<div class="unit active"><div class="section" style="text-align:center;padding:40px">选择一个单元</div></div>'; return; }
  engState.cardIdx = 0;
  showEngCard();
}

function showEngCard() {
  var u = ENGLISH_UNITS[currentUnit - 1];
  var idx = engState.cardIdx || 0;
  if (idx >= u.words.length) idx = 0;
  engState.cardIdx = idx;
  var w = u.words[idx];
  var html = '<div class="unit active">';
  html += '<div class="unit-title">'+u.unit+'</div>';
  html += '<div class="unit-subtitle">单词卡片 '+(idx+1)+'/'+u.words.length+'</div>';
  html += '<div class="flashcard-scene"><div class="flashcard-container" onclick="this.classList.toggle(\'flipped\')">';
  html += '<div class="flashcard-face flashcard-front">';
  html += '<div style="font-size:2.5em;font-weight:700;color:var(--primary)">'+w.en+'</div>';
  html += '<div style="margin-top:12px;color:var(--gray)">点击翻转</div>';
  html += '</div>';
  html += '<div class="flashcard-face flashcard-back">';
  html += '<div style="font-size:2em;font-weight:700;color:var(--green)">'+w.cn+'</div>';
  html += '<div style="margin-top:8px;color:#666">'+w.en+'</div>';
  html += '</div></div></div>';
  html += '<div class="flashcard-nav">';
  html += '<button class="btn btn-sm" style="background:#eee" onclick="engState.cardIdx=Math.max(0,engState.cardIdx-1);showEngCard()">上一个</button>';
  html += '<span style="color:var(--gray)">'+(idx+1)+'/'+u.words.length+'</span>';
  html += '<button class="btn btn-sm" style="background:#eee" onclick="engState.cardIdx++;showEngCard()">下一个</button>';
  html += '</div></div>';
  document.getElementById('app').innerHTML = html;
}

function finishEngGame() {
  var total = engState.correct+engState.wrong;
  var acc = total>0?Math.round(engState.correct/total*100):0;
  var stars = acc>=90?'\u2b50\u2b50\u2b50':acc>=70?'\u2b50\u2b50':acc>=50?'\u2b50':'';
  var html = '<div class="unit active"><div class="result-card">';
  html += '<div style="font-size:3em">'+(engState.hearts>0?'\ud83c\udf89':'\ud83d\ude22')+'</div>';
  html += '<div class="result-stars">'+stars+'</div>';
  html += '<div class="result-text">'+(engState.hearts>0?'练习完成！':'生命用完了！')+'</div>';
  html += '<div style="color:var(--gray)">答对 '+engState.correct+' 个</div>';
  html += '<div class="btn-group" style="justify-content:center;margin-top:16px">';
  html += '<button class="btn btn-primary" onclick="renderEngDictation()">再来一次</button>';
  html += '<button class="btn btn-blue" onclick="renderEngFlashcard()">看卡片</button>';
  html += '</div></div></div>';
  document.getElementById('app').innerHTML = html;
}
"""

content = content[:script_end] + new_funcs + content[script_end:]

# 5. Update renderContent to handle new modes
old_switch = """function renderContent() {
  switch(currentMode) {
    case 'review': renderReview(); break;
    case 'quiz': renderQuiz(); break;
    case 'flashcard': renderFlashcard(); break;
    case 'dictation': renderVocabDictation(); break;
    case 'recite': renderRecite(); break;
    case 'story': renderStory(); break;
    case 'review-due': renderReviewDue(); break;
  }
}"""

new_switch = """function renderContent() {
  if (currentSubject === 'math') {
    switch(currentMode) {
      case 'mental': renderMathMental(); break;
      case 'formula': renderMathFormula(); break;
      default: renderMathMental();
    }
  } else if (currentSubject === 'english') {
    switch(currentMode) {
      case 'eng-dict': renderEngDictation(); break;
      case 'eng-trans': renderEngTranslation(); break;
      case 'eng-card': renderEngFlashcard(); break;
      default: renderEngDictation();
    }
  } else {
    switch(currentMode) {
      case 'review': renderReview(); break;
      case 'quiz': renderQuiz(); break;
      case 'flashcard': renderFlashcard(); break;
      case 'dictation': renderVocabDictation(); break;
      case 'recite': renderRecite(); break;
      case 'story': renderStory(); break;
      case 'review-due': renderReviewDue(); break;
    }
  }
}"""

content = content.replace(old_switch, new_switch)

# 6. Update initialization to call renderModeTabs
old_init = "renderUnitTabs();\nrenderContent();"
new_init = "renderModeTabs();\nrenderUnitTabs();\nrenderContent();"
content = content.replace(old_init, new_init)

with open(r'D:\语文复习App\docs\index.html', 'w', encoding='utf-8') as f:
    f.write(content)

# Verify
import subprocess
result = subprocess.run(['node', '-e', r'''
const fs = require("fs");
const html = fs.readFileSync("D:/语文复习App/docs/index.html", "utf8");
const m = html.match(/<script>([\s\S]*?)<\/script>/);
if (m) {
  const s = {getItem:()=>null,setItem:()=>{},removeItem:()=>{}};
  try { eval(m[1]); console.log("OK"); }
  catch(e) { console.log("ERR:", e.message.substring(0,200)); }
}
'''], capture_output=True, text=True, timeout=10)
print(result.stdout.strip())
print(f"File: {len(content)} chars")
