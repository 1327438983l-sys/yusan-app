"""Patch v3.1: textbook vocabulary + speech recitation + fix"""
import re

with open(r'D:\语文复习App\docs\index.html', 'r', encoding='utf-8') as f:
    content = f.read()

# === 1. Add textbook vocabulary data before POEM_STORIES ===
vocab_data = """// Textbook vocabulary organized by lesson (课本词语表)
var TEXTBOOK_VOCAB = [
  {lesson:'第2课 燕子', words:['燕子','乌黑','剪刀','活泼','轻风','洒落','赶集','光彩夺目','春光','偶尔','闲散','纤细','电线']},
  {lesson:'第3课 荷花', words:['荷花','公园','清香','赶紧','荷叶','莲蓬','破裂','姿势','画家','本领','了不起','微风','停止']},
  {lesson:'第6课 灰雀', words:['友情','认识','忠诚','驯良','善良','温和','答谢','花言巧语','着急','相信','尘土','凶恶','恶狠狠','猎人','收拾']},
  {lesson:'第7课 鹿角和鹿腿', words:['痛快','匀称','精美','别致','眉头','没精打采','机灵','灰心丧气','机会','叹气','逃生']},
  {lesson:'第9课 海底世界', words:['宁静','器官','是否','窃窃私语','危险','方法','肌肉','攻击','利用','后退','免费','差异','清楚','奇异']},
  {lesson:'第10课 蜜蜂', words:['实验','验证','记号','减少','阻力','大约','包括','检查','至少','迷失','无误','逆风','陌生','景物','能力']}
];
"""

content = content.replace('// ==================== DATA ====================\n', '// ==================== DATA ====================\n' + vocab_data)

# === 2. Add speech recognition CSS ===
css_add = """/* Speech Recognition */
.recite-result{background:#f8f9fa;border-radius:12px;padding:16px;margin:12px 0;text-align:center}
.recite-score{font-size:2em;font-weight:700;margin:8px 0}
.recite-score.perfect{color:var(--green)}
.recite-score.good{color:var(--primary)}
.recite-score.bad{color:var(--red)}
.recite-transcript{font-size:1.05em;line-height:1.8;margin:12px 0;text-align:left;background:#fff;padding:12px;border-radius:8px;border:1px solid #eee;min-height:60px;white-space:pre-wrap}
.recite-transcript .correct-char{color:var(--green);font-weight:600}
.recite-transcript .wrong-char{color:var(--red);text-decoration:line-through;font-weight:600}
.recite-transcript .miss-char{color:var(--gray);background:#fff3cd;padding:0 2px;border-radius:2px}
.mic-btn{width:72px;height:72px;border-radius:50%;border:3px solid var(--red);background:#fff;color:var(--red);font-size:1.8em;cursor:pointer;transition:all .2s;display:flex;align-items:center;justify-content:center;margin:12px auto}
.mic-btn:hover{background:var(--red);color:#fff}
.mic-btn.listening{background:var(--red);color:#fff;animation:pulse 1s infinite}
/* Vocab Vocab */
.vocab-section{margin:12px 0}
.vocab-lesson{font-size:1em;font-weight:600;color:var(--primary);margin:12px 0 6px;padding:6px 12px;background:rgba(230,126,34,0.08);border-radius:6px}
.vocab-words{display:flex;flex-wrap:wrap;gap:6px;margin:6px 0 12px}
.vocab-tag{background:#f0f9ff;border:1px solid #d0e8ff;border-radius:6px;padding:4px 10px;font-size:0.9em;cursor:default}
.vocab-game-word{font-size:1.4em;font-weight:700;color:var(--primary);margin:8px 0}
"""
content = content.replace('/* Game Dictation */', css_add + '\n/* Game Dictation */')

# === 3. Add speech recognition + vocab game JS before </script> ===
script_end = content.rfind('</script>')

speech_js = """
// ==================== SPEECH RECOGNITION ====================
var reciteRecognition = null;

function startReciteListen(poemTitle) {
  var SR = window.SpeechRecognition || window.webkitSpeechRecognition;
  if (!SR) { alert('您的浏览器不支持语音识别，请用Chrome打开'); return; }
  var u = UNITS.find(function(x){return x.num===currentUnit;});
  var poem = u.review.poems.find(function(p){return p.title===poemTitle;});
  if (!poem) return;
  var target = poem.content.replace(/\\n/g,'').replace(/[，。！？、；：""''《》（）\\s]/g,'');
  
  var resultDiv = document.getElementById('reciteResult_'+poemTitle);
  var micBtn = document.getElementById('micBtn_'+poemTitle);
  if (resultDiv) resultDiv.innerHTML = '<div style="color:var(--red);font-size:1.1em">正在听您背诵...</div>';
  if (micBtn) micBtn.classList.add('listening');
  
  if (reciteRecognition) { try{reciteRecognition.stop();}catch(e){} }
  reciteRecognition = new SR();
  reciteRecognition.lang = 'zh-CN';
  reciteRecognition.continuous = true;
  reciteRecognition.interimResults = true;
  var finalT = '';
  
  reciteRecognition.onresult = function(ev) {
    var interim = '';
    for (var i=ev.resultIndex;i<ev.results.length;i++) {
      if (ev.results[i].isFinal) finalT += ev.results[i][0].transcript;
      else interim += ev.results[i][0].transcript;
    }
    if (resultDiv) resultDiv.innerHTML = '<div style="color:var(--gray)">'+(finalT+interim)+'</div>';
  };
  reciteRecognition.onend = function() {
    if (micBtn) micBtn.classList.remove('listening');
    if (finalT) gradeRecite(finalT, poemTitle);
  };
  reciteRecognition.onerror = function(e) {
    if (micBtn) micBtn.classList.remove('listening');
    if (resultDiv) resultDiv.innerHTML = '<div style="color:var(--gray)">'+(e.error==='no-speech'?'没有听到声音，再试一次？':'识别出错：'+e.error)+'</div>';
  };
  reciteRecognition.start();
  setTimeout(function(){try{reciteRecognition.stop();}catch(e){}},30000);
}

function gradeRecite(spoken, poemTitle) {
  var u = UNITS.find(function(x){return x.num===currentUnit;});
  var poem = u.review.poems.find(function(p){return p.title===poemTitle;});
  if (!poem) return;
  var target = poem.content.replace(/\\n/g,'').replace(/[，。！？、；：""''《》（）\\s,.!?;:'"()]/g,'');
  var spokenClean = spoken.replace(/[，。！？、；：""''《》（）\\s,.!?;:'"()\\u3000]/g,'');
  
  var m=target.length, n=spokenClean.length;
  var dp=[];for(var i=0;i<=m;i++){dp[i]=[];for(var j=0;j<=n;j++){if(i===0||j===0)dp[i][j]=0;else if(target[i-1]===spokenClean[j-1])dp[i][j]=dp[i-1][j-1]+1;else dp[i][j]=Math.max(dp[i-1][j],dp[i][j-1]);}}
  var match=dp[m][n], acc=Math.round(match/m*100);
  
  var i2=m,j2=n,tC=[],sC=[];
  while(i2>0&&j2>0){if(target[i2-1]===spokenClean[j2-1]){tC.unshift({ch:target[i2-1],t:'c'});sC.unshift({ch:spokenClean[j2-1],t:'c'});i2--;j2--;}else if(dp[i2-1][j2]>dp[i2][j2-1]){tC.unshift({ch:target[i2-1],t:'m'});i2--;}else{sC.unshift({ch:spokenClean[j2-1],t:'w'});j2--;}}
  while(i2>0){tC.unshift({ch:target[i2-1],t:'m'});i2--;}
  while(j2>0){sC.unshift({ch:spokenClean[j2-1],t:'w'});j2--;}
  
  function fmt(arr){var h='';arr.forEach(function(c,ci){var cls=c.t==='c'?'correct-char':c.t==='m'?'miss-char':'wrong-char';h+='<span class="'+cls+'">'+c.ch+'</span>';if((ci+1)%15===0)h+='<br>';});return h;}
  var sc=acc>=90?'perfect':acc>=60?'good':'bad';
  var em=acc>=90?'\u2b50':acc>=60?'\ud83d\udcaa':'\ud83d\udcdd';
  var cm=acc>=90?'背得很棒！':acc>=60?'还不错，再练练！':'加油哦，多读几遍再试！';
  
  var html='<div class="recite-result">';
  html+='<div style="font-size:1.2em">'+em+'</div>';
  html+='<div class="recite-score '+sc+'">'+acc+'%</div>';
  html+='<div style="color:#666">'+match+'/'+m+' 个字匹配，'+cm+'</div>';
  html+='<div style="margin-top:12px;text-align:left">';
  html+='<div style="font-size:0.85em;color:var(--gray);margin-bottom:4px">你背的：</div>';
  html+='<div class="recite-transcript">'+fmt(sC)+'</div>';
  html+='<div style="font-size:0.85em;color:var(--gray);margin:8px 0 4px">原文：</div>';
  html+='<div class="recite-transcript">'+fmt(tC)+'</div>';
  html+='</div>';
  html+='<div class="btn-group" style="justify-content:center;margin-top:12px">';
  html+='<button class="btn btn-primary btn-sm" onclick="startReciteListen(\\''+poemTitle+'\\')">再背一次</button>';
  html+='<button class="btn btn-green btn-sm" onclick="speakPoem(\\''+poemTitle+'\\',0.6)">先听一遍</button>';
  html+='</div></div>';
  if (resultDiv) resultDiv.innerHTML = html;
  if (acc>=90) addPoints(30); else if (acc>=60) addPoints(15);
  updateGameStats();
}

// ==================== VOCAB DICTATION (课本词语表) ====================
var vocabGameState = {lessonIdx:0, wordIdx:0, hearts:3, correct:0, wrong:0, score:0};

function renderVocabDictation() {
  var html = '<div class="unit active">';
  html += '<div class="unit-title">默写词语表</div>';
  html += '<div class="unit-subtitle">按课文顺序默写课本词语</div>';
  vocabGameState = {lessonIdx:0, wordIdx:0, hearts:3, correct:0, wrong:0, score:0};
  html += '<div class="vocab-section">';
  TEXTBOOK_VOCAB.forEach(function(sec, i) {
    html += '<div class="vocab-lesson">'+sec.lesson+' ('+sec.words.length+'词)</div>';
    html += '<div class="vocab-words">';
    sec.words.forEach(function(w){ html += '<span class="vocab-tag">'+w+'</span>'; });
    html += '</div>';
  });
  html += '</div>';
  html += '<div class="btn-group" style="justify-content:center"><button class="btn btn-primary" onclick="startVocabGame()">开始默写</button></div>';
  html += '</div>';
  document.getElementById('app').innerHTML = html;
}

function startVocabGame() {
  vocabGameState = {lessonIdx:0, wordIdx:0, hearts:3, correct:0, wrong:0, score:0, answered:{}};
  renderVocabQuestion();
}

function renderVocabQuestion() {
  var vg = vocabGameState;
  if (vg.lessonIdx >= TEXTBOOK_VOCAB.length) { finishVocabGame(); return; }
  var sec = TEXTBOOK_VOCAB[vg.lessonIdx];
  if (vg.wordIdx >= sec.words.length) { vg.lessonIdx++; vg.wordIdx=0; renderVocabQuestion(); return; }
  var word = sec.words[vg.wordIdx];
  
  // Generate pinyin hint (first char only)
  var hint = word.charAt(0);
  
  var html = '<div class="unit active">';
  // Hearts
  html += '<div class="hearts">';
  for(var i=0;i<3;i++) html += '<span class="heart '+(i<vg.hearts?'':'lost')+'">'+(i<vg.hearts?'\u2764\ufe0f':'\u2764')+'</span>';
  html += '</div>';
  html += '<div style="text-align:center;color:var(--gray);font-size:0.9em">'+sec.lesson+' | 第 '+(vg.wordIdx+1)+'/'+sec.words.length+' 词</div>';
  html += '<div class="game-question">';
  html += '<div style="font-size:0.9em;color:var(--gray);margin-bottom:4px">写出这个词（'+word.length+'个字）：</div>';
  html += '<div class="vocab-game-word">____'+('____').repeat(word.length-1)+'</div>';
  html += '<input class="game-input" id="vocabInput" placeholder="请输入" autocomplete="off" autocapitalize="off">';
  html += '<div class="game-answer" id="vocabAnswer" style="display:none"></div>';
  html += '</div>';
  html += '<div style="text-align:center;margin-top:16px"><button class="btn btn-primary" onclick="checkVocabAnswer()">确认</button></div>';
  html += '</div>';
  document.getElementById('app').innerHTML = html;
  var inp = document.getElementById('vocabInput');
  inp.focus();
  inp.onkeydown = function(e){ if(e.key==='Enter') checkVocabAnswer(); };
}

function checkVocabAnswer() {
  var vg = vocabGameState;
  var sec = TEXTBOOK_VOCAB[vg.lessonIdx];
  var word = sec.words[vg.wordIdx];
  var inp = document.getElementById('vocabInput');
  var ans = document.getElementById('vocabAnswer');
  var val = inp.value.trim();
  if (!val) return;
  
  var key = vg.lessonIdx+'-'+vg.wordIdx;
  if (vg.answered[key] !== undefined) return;
  vg.answered[key] = true;
  
  if (val === word) {
    vg.correct++;
    vg.score += 10;
    inp.classList.add('correct');
    ans.innerHTML = '<span class="correct-text">\u2705 答对了！</span>';
    addPoints(10);
  } else {
    vg.wrong++;
    vg.hearts--;
    inp.classList.add('wrong');
    ans.innerHTML = '\u274c 正确答案：<span class="correct-text">'+word+'</span>';
  }
  ans.style.display = 'block';
  inp.disabled = true;
  updateGameStats();
  
  setTimeout(function(){
    if (vg.hearts <= 0) { finishVocabGame(); return; }
    vg.wordIdx++;
    renderVocabQuestion();
  }, 1200);
}

function finishVocabGame() {
  var vg = vocabGameState;
  var total = 0;
  TEXTBOOK_VOCAB.forEach(function(s){total+=s.words.length;});
  var acc = Math.round(vg.correct / (vg.correct+vg.wrong) * 100);
  var stars = acc>=90?'\u2b50\u2b50\u2b50':acc>=70?'\u2b50\u2b50':acc>=50?'\u2b50':'';
  
  var html = '<div class="unit active">';
  html += '<div class="result-card">';
  html += '<div style="font-size:3em">'+(vg.hearts>0?'\ud83c\udf89':'\ud83d\ude22')+'</div>';
  html += '<div class="result-stars">'+stars+'</div>';
  html += '<div class="result-text">'+(vg.hearts>0?'默写完成！':'生命用完了！')+'</div>';
  html += '<div style="color:var(--gray)">答对 '+vg.correct+' 个，错误 '+vg.wrong+' 个，得分 '+vg.score+'</div>';
  html += '<div class="btn-group" style="justify-content:center;margin-top:16px">';
  html += '<button class="btn btn-primary" onclick="startVocabGame()">再来一次</button>';
  html += '<button class="btn btn-blue" onclick="renderVocabDictation()">返回</button>';
  html += '</div></div></div>';
  document.getElementById('app').innerHTML = html;
}
"""

content = content[:script_end] + speech_js + content[script_end:]

# === 4. Add vocab dictation CSS for vocab-game-word ===
# Already added in css_add above

# === 5. Update switchMode ===
content = content.replace(
    "case 'dictation': renderDictation(); break;",
    "case 'dictation': renderVocabDictation(); break;"
)

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
  catch(e) { 
    if (e.message.includes('document') || e.message.includes('speechSynthesis') || e.message.includes('is not defined'))
      console.log("OK (browser): " + e.message.substring(0,50));
    else console.log("ERR:", e.message.substring(0,200));
  }
} else { console.log("NO SCRIPT"); }
'''], capture_output=True, text=True, timeout=10)
print(result.stdout.strip())
print(f"File: {len(content)} chars")
