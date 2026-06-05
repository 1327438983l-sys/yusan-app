"""Patch index.html: game dictation + daily story + recitation mode"""
import re

with open(r'D:\语文复习App\docs\index.html', 'r', encoding='utf-8') as f:
    content = f.read()

# === 1. Add new CSS before </style> ===
new_css = """
/* Game Dictation */
.level-grid{display:grid;grid-template-columns:repeat(3,1fr);gap:12px;max-width:400px;margin:20px auto}
.level-btn{padding:16px;border-radius:12px;border:2px solid #ddd;background:#fff;cursor:pointer;text-align:center;transition:all .2s;position:relative}
.level-btn:hover{transform:translateY(-2px);box-shadow:var(--shadow)}
.level-btn.locked{opacity:0.4;cursor:not-allowed}
.level-btn.locked::after{content:'🔒';position:absolute;top:8px;right:8px;font-size:0.8em}
.level-btn .level-num{font-size:1.5em;font-weight:700;color:var(--primary)}
.level-btn .level-stars{margin-top:4px;font-size:0.9em}
.level-btn.completed{border-color:var(--green);background:#f0fff4}
.hearts{display:flex;justify-content:center;gap:6px;font-size:1.8em;margin:12px 0}
.heart{transition:all .3s}
.heart.lost{opacity:0.2;transform:scale(0.8)}
.game-question{background:var(--card);border-radius:16px;padding:24px;text-align:center;box-shadow:var(--shadow-lg);max-width:400px;margin:0 auto}
.game-pinyin{font-size:2.5em;color:var(--primary);font-weight:700;margin-bottom:16px;letter-spacing:3px}
.game-input{border:3px solid #ddd;border-radius:12px;padding:16px;font-size:2em;width:200px;text-align:center;font-family:'KaiTi','STKaiti',serif;outline:none;transition:all .3s}
.game-input:focus{border-color:var(--primary);box-shadow:0 0 0 4px rgba(230,126,34,0.15)}
.game-input.correct{border-color:var(--green);background:#d4edda;animation:correctBounce .4s ease}
.game-input.wrong{border-color:var(--red);background:#f8d7da;animation:wrongShake .4s ease}
.game-answer{margin-top:12px;font-size:1.1em;color:#666}
.game-answer .correct-text{color:var(--green);font-weight:700;font-size:1.4em}
.result-card{background:var(--card);border-radius:16px;padding:32px;text-align:center;box-shadow:var(--shadow-lg);max-width:400px;margin:20px auto}
.result-stars{font-size:3em;margin:16px 0}
.result-text{font-size:1.2em;color:#555;margin:8px 0}
@keyframes correctBounce{0%{transform:scale(1)}50%{transform:scale(1.1)}100%{transform:scale(1)}}
@keyframes wrongShake{0%,100%{transform:translateX(0)}25%{transform:translateX(-8px)}75%{transform:translateX(8px)}}
/* Daily Story */
.story-card{background:var(--card);border-radius:16px;padding:24px;box-shadow:var(--shadow-lg);max-width:600px;margin:0 auto}
.story-title{font-size:1.3em;font-weight:700;color:var(--primary);margin-bottom:12px;text-align:center}
.story-body{font-size:1.05em;line-height:2;margin-bottom:16px;text-indent:2em}
.story-streak{display:flex;align-items:center;justify-content:center;gap:8px;margin:12px 0;font-size:0.9em}
.story-streak .streak-num{font-size:1.5em;font-weight:700;color:var(--primary)}
/* Recitation */
.recite-card{background:var(--card);border-radius:16px;padding:24px;box-shadow:var(--shadow);max-width:500px;margin:0 auto 16px}
.recite-poem{font-size:1.3em;line-height:2.2;text-align:center;margin:16px 0;letter-spacing:1px}
.recite-controls{display:flex;justify-content:center;gap:12px;margin-top:16px}
.play-btn{width:60px;height:60px;border-radius:50%;border:none;font-size:1.5em;cursor:pointer;transition:all .2s;display:flex;align-items:center;justify-content:center}
.play-btn:hover{transform:scale(1.1)}
.play-btn.playing{animation:pulse 1s infinite}
@keyframes pulse{0%,100%{box-shadow:0 0 0 0 rgba(230,126,34,0.4)}50%{box-shadow:0 0 0 12px rgba(230,126,34,0)}}
.speed-btn{padding:6px 14px;border:2px solid #ddd;border-radius:20px;background:#fff;cursor:pointer;font-size:0.85em;transition:all .2s}
.speed-btn.active{border-color:var(--primary);background:var(--primary);color:#fff}
"""
content = content.replace('/* Mobile */', new_css + '/* Mobile */')

# === 2. Update mode tabs ===
old_tabs = """  <div class="mode-tab active" data-mode="review" onclick="switchMode('review')">📚复习清单</div>
  <div class="mode-tab" data-mode="quiz" onclick="switchMode('quiz')">📝单元测试</div>
  <div class="mode-tab" data-mode="flashcard" onclick="switchMode('flashcard')">🃏闪卡记忆</div>
  <div class="mode-tab" data-mode="dictation" onclick="switchMode('dictation')">✍️字词默写</div>
  <div class="mode-tab" data-mode="review-due" onclick="switchMode('review-due')">📊今日复习</div>"""
new_tabs = """  <div class="mode-tab active" data-mode="review" onclick="switchMode('review')">📚复习清单</div>
  <div class="mode-tab" data-mode="recite" onclick="switchMode('recite')">🎤背诵朗读</div>
  <div class="mode-tab" data-mode="quiz" onclick="switchMode('quiz')">📝单元测试</div>
  <div class="mode-tab" data-mode="flashcard" onclick="switchMode('flashcard')">🃏闪卡记忆</div>
  <div class="mode-tab" data-mode="dictation" onclick="switchMode('dictation')">✍️闯关默写</div>
  <div class="mode-tab" data-mode="story" onclick="switchMode('story')">📖每日故事</div>
  <div class="mode-tab" data-mode="review-due" onclick="switchMode('review-due')">📊今日复习</div>"""
content = content.replace(old_tabs, new_tabs)

# === 3. Add daily story data and recite/dictation/story functions ===
# Find the end of the script (before </script>)
script_end_marker = '</script>'
idx = content.rfind(script_end_marker)

new_functions = r"""
// ==================== RECITATION MODE ====================
function renderRecite() {
  const u = UNITS.find(x => x.num === currentUnit);
  if (!u.review.poems.length) {
    document.getElementById('app').innerHTML = '<div class="unit active"><div class="section" style="text-align:center;padding:40px"><p style="font-size:1.2em;color:var(--gray)">本单元没有古诗，切换到其他单元试试 📚</p></div></div>';
    return;
  }
  let html = '<div class="unit active">';
  html += '<div class="unit-title">' + u.title + ' \xb7 背诵朗读</div>';
  html += '<div class="unit-subtitle">听一听标准朗读，跟着背一背 🎧</div>';
  u.review.poems.forEach(function(p, i) {
    html += '<div class="recite-card">';
    html += '<div style="font-size:1.1em;font-weight:700;color:var(--primary)">《' + p.title + '》</div>';
    html += '<div style="color:var(--gray);font-size:0.9em;margin:4px 0">' + p.author + '</div>';
    html += '<div class="recite-poem">' + p.content.replace(/\n/g, '<br>') + '</div>';
    html += '<div class="recite-controls">';
    html += '<button class="play-btn btn-primary" onclick="speakPoem(\'' + p.title + '\', 0.8)" title="正常速度">▶</button>';
    html += '<button class="play-btn btn-green" onclick="speakPoem(\'' + p.title + '\', 0.5)" title="慢速" style="font-size:1.2em">🐢</button>';
    html += '<button class="play-btn" onclick="stopSpeak()" title="停止" style="background:#eee;font-size:1.2em">⏹</button>';
    html += '</div>';
    html += '<div style="margin-top:10px;padding:8px 12px;background:#fff8e1;border-radius:8px;font-size:0.85em;line-height:1.7;border-left:3px solid #f39c12">';
    html += '<b style="color:#e67e22">\ud83d\udcd6 诗人小故事</b><br>' + (POEM_STORIES[p.title] || '') + '</div>';
    html += '</div>';
  });
  html += '</div>';
  document.getElementById('app').innerHTML = html;
}

function speakPoem(title, rate) {
  stopSpeak();
  var u = UNITS.find(function(x) { return x.num === currentUnit; });
  var poem = u.review.poems.find(function(p) { return p.title === title; });
  if (!poem) return;
  var text = poem.title + '。' + poem.author + '。' + poem.content.replace(/\n/g, '。');
  var u = new SpeechSynthesisUtterance(text);
  u.lang = 'zh-CN';
  u.rate = rate || 0.8;
  u.pitch = 1.1;
  speechSynthesis.speak(u);
}
function stopSpeak() { speechSynthesis.cancel(); }

// ==================== DAILY STORY ====================
var DAILY_STORIES = [
  {t:'小蝌蚪找妈妈', body:'池塘里有一群小蝌蚪，大大的脑袋，黑灰色的身子，甩着长长的尾巴，快活地游来游去。小蝌蚪看见鸭妈妈带着小鸭子在水里游来游去，就迎上去问：\u201c鸭阿姨，我们的妈妈在哪里呀？\u201d鸭妈妈说：\u201c你们的妈妈四条腿，宽嘴巴。你们到那边去找吧！\u201d小蝌蚪游哇游，游了好久，终于找到了自己的妈妈\u2014\u2014青蛙。原来他们长大后会变成青蛙呀！', q:'小蝌蚪的妈妈是谁？', opts:['鸭子','金鱼','青蛙','乌龟'], ans:2},
  {t:'曹冲称象', body:'古时候有个叫曹操的人，别人送给他一头大象。曹操想知道这头大象有多重，可是没有人能称出这么大的东西。曹操的儿子曹冲才七岁，他站出来说：\u201c我有办法！\u201d他让人把大象赶到一艘大船上，看船身下沉多少，然后在船舷上做记号。再把大象牵上岸，往船上装石头，直到船沉到记号的地方。最后称石头的重量，就知道大象有多重了。曹操听了很高兴，让人照曹冲的办法去做。', q:'曹冲用什么办法称大象？', opts:['用很大的秤','用石头代替大象','把大象切开称','问别人'], ans:1},
  {t:'铁杵磨针', body:'李白小时候不爱学习，有一天他逃学出去玩，看见一位老婆婆在河边磨一根铁棒。李白问：\u201c老婆婆，您磨铁棒干什么呀？\u201d老婆婆说：\u201c我想把它磨成一根绣花针。\u201d李白惊讶地说：\u201c这么粗的铁棒，怎么可能磨成针呢？\u201d老婆婆笑着说：\u201c只要功夫深，铁杵也能磨成针呀！\u201d李白听了很受启发，从此认真读书，后来成了伟大的诗人。', q:'这个故事告诉我们什么道理？', opts:['铁棒很硬','只要有恒心就能成功','老婆婆很有钱','李白不喜欢学习'], ans:1},
  {t:'孔融让梨', body:'孔融四岁的时候，和哥哥们一起吃梨。孔融总是拿最小的梨，把大的留给哥哥们。大人问他：\u201c你为什么不拿大的呢？\u201d孔融说：\u201c我年纪小，应该吃小的，大的留给哥哥们吃。\u201d大人又问：\u201c那弟弟比你小呀？\u201d孔融说：\u201c弟弟比我小，我是哥哥，应该让着弟弟。\u201d大家都夸孔融是个懂事的好孩子。', q:'孔融为什么总是拿最小的梨？', opts:['他只喜欢吃小的','他想让给哥哥和弟弟','他不够高','梨太重了'], ans:1},
  {t:'闻鸡起舞', body:'东晋时期，有两个好朋友叫祖逖和刘琨。他们年轻时一起在朝廷做官，住在同一个房间里。有一天半夜，祖逖听见鸡叫，就把刘琨叫醒说：\u201c别人都说半夜鸡叫不吉利，我觉得这是在催我们起床练武呢！\u201d从此以后，他们每天听到鸡叫就起床练剑。不管刮风下雨，从不间断。后来祖逖成了著名的大将军。', q:'祖逖半夜听到鸡叫后做了什么？', opts:['继续睡觉','起床练武','去抓鸡','叫别人起床'], ans:1},
  {t:'大禹治水', body:'很久很久以前，洪水淹没了村庄和田野。禹的父亲用堵的办法治水，花了九年也没有成功。禹继承了父亲的事业，他用疏导的办法\u2014\u2014挖开河道，让洪水流到大海里去。禹一心治水，十三年里三次经过自己家门口都没有进去。他的妻子和儿子在家等他，他只是远远地看一眼就走了。最终禹成功治好了洪水，人们都叫他\u201c大禹\u201d。', q:'大禹治水成功用了什么方法？', opts:['堵住河流','用船运水','疏导河道让水流入大海','用水泵'], ans:2},
  {t:'愚公移山', body:'从前有个叫愚公的老人，家门前有两座大山挡住了出路。愚公决心把山挖掉。有人笑话他说：\u201c你太傻了，这两座山这么高，你怎么挖得完呢？\u201d愚公说：\u201c我死了有儿子，儿子死了有孙子，子子孙孙无穷无尽，总有一天会挖完的！\u201d愚公的精神感动了天帝，天帝派神仙把两座山搬走了。', q:'愚公为什么要移山？', opts:['山上有宝藏','山挡住了出路','他想种地','有人逼他'], ans:1},
  {t:'守株待兔', body:'宋国有个农夫，有一天他在田里干活，忽然看见一只兔子飞快地跑过来，撞在田边的树桩上死了。农夫白捡了一只兔子，心想：\u201c要是天天有兔子撞死在树桩上，那该多好啊！\u201d从此他放下农具，天天守在树桩旁边等兔子。结果再也没有兔子撞过来，他的庄稼也荒废了。', q:'农夫最后的结果怎样？', opts:['又捡到很多兔子','庄稼荒废了','树桩长出了新芽','他搬走了'], ans:1},
  {t:'画蛇添足', body:'有几个人比赛画蛇，谁先画完谁就能得到一壶好酒。有一个人画得特别快，第一个画完了。他看看别人还没画完，就得意地说：\u201c我还能给蛇画上脚呢！\u201d于是他左手拿着酒壶，右手给蛇画起了脚。这时候另一个人也画完了，夺过酒壶说：\u201c蛇本来就没有脚，你画了脚就不是蛇了！\u201d说完把酒喝了。', q:'画蛇添足的人为什么没有喝到酒？', opts:['他画得太慢了','蛇本来没有脚，他多此一举','酒被别人偷了','他不想喝'], ans:1},
  {t:'狐假虎威', body:'老虎抓到一只狐狸，正要吃它。狐狸说：\u201c你不能吃我！天帝派我做百兽之王，你要是吃了我，就是违抗天帝的命令！不信的话，你跟在我后面走，看看动物们怕不怕我。\u201d老虎半信半疑，就跟在狐狸后面走。果然，动物们看见它们都吓得跑掉了。老虎信以为真，放了狐狸。其实动物们怕的是老虎，不是狐狸呀！', q:'动物们其实怕的是谁？', opts:['狐狸','天帝','老虎','猎人'], ans:2},
  {t:'精卫填海', body:'炎帝有一个女儿叫女娃，她到东海去游玩，不幸被海水淹死了。女娃的灵魂变成了一只小鸟，名叫精卫。精卫每天从西山上衔来小石子和小树枝，一次又一次地投到东海里。她想：\u201c我要把东海填平，不让它再夺走别人的生命！\u201d虽然东海很大很大，但精卫从不放弃，一直坚持着。', q:'精卫为什么要填海？', opts:['她喜欢玩石子','她被东海淹死，想报仇','她想造一座岛','有人让她这么做'], ans:1},
  {t:'卧冰求鲤', body:'晋朝有个叫王祥的人，他的继母对他很不好。有一年冬天，继母生病了，想吃鲤鱼。可是河面结了厚厚的冰，根本捕不到鱼。王祥就脱了衣服躺在冰面上，想用自己的体温把冰融化。他的孝心感动了上天，冰面突然裂开，两条鲤鱼跳了出来。王祥高高兴兴地把鱼带回家给继母吃。', q:'王祥为什么躺在冰上？', opts:['他很热','他想用体温融化冰面捕鱼','他在做游戏','冰面很滑'], ans:1}
];

function renderStory() {
  var dayOfYear = Math.floor((Date.now() - new Date(new Date().getFullYear(),0,0)) / 86400000);
  var storyIdx = dayOfYear % DAILY_STORIES.length;
  var story = DAILY_STORIES[storyIdx];
  
  // Streak
  var streak = parseInt(localStorage.getItem('story_streak') || '0');
  var lastRead = localStorage.getItem('story_last_read');
  var today = new Date().toDateString();
  if (lastRead === today) {
    // Already read today
  } else if (lastRead === new Date(Date.now() - 86400000).toDateString()) {
    streak++;
  } else {
    streak = 1;
  }
  localStorage.setItem('story_streak', streak);
  
  var html = '<div class="unit active">';
  html += '<div class="unit-title">📖 每日小故事</div>';
  html += '<div class="story-streak">🔥 连续阅读 <span class="streak-num">' + streak + '</span> 天</div>';
  html += '<div class="story-card">';
  html += '<div class="story-title">' + story.t + '</div>';
  html += '<div class="story-body">' + story.body + '</div>';
  html += '<div style="background:#f0f7ff;border-radius:12px;padding:16px;margin-top:16px">';
  html += '<div style="font-weight:600;color:var(--blue);margin-bottom:8px">\ud83d\udcdd 读一读，想一想</div>';
  html += '<div style="margin-bottom:10px">' + story.q + '</div>';
  story.opts.forEach(function(opt, i) {
    html += '<div class="quiz-opt" onclick="checkStoryAnswer(this,' + i + ',' + story.ans + ')" style="margin:4px 0">' + String.fromCharCode(65+i) + '. ' + opt + '</div>';
  });
  html += '<div id="storyFeedback" style="display:none;margin-top:10px;padding:8px 12px;border-radius:8px;font-size:0.9em"></div>';
  html += '</div>';
  html += '<div class="btn-group" style="justify-content:center;margin-top:16px">';
  html += '<button class="btn btn-primary" onclick="speakStory(\'' + story.t + '\')">\u25b6 \u542c\u6545\u4e8b</button>';
  html += '<button class="btn btn-green" onclick="switchMode(\'story\')">\ud83d\udd04 \u660e\u5929\u518d\u6765</button>';
  html += '</div>';
  html += '</div></div>';
  document.getElementById('app').innerHTML = html;
}

function checkStoryAnswer(el, chosen, correct) {
  var opts = el.parentElement.querySelectorAll('.quiz-opt');
  if (el.classList.contains('correct') || el.classList.contains('wrong')) return;
  opts.forEach(function(o, i) {
    o.style.pointerEvents = 'none';
    if (i === correct) o.classList.add('correct');
    if (i === chosen && i !== correct) o.classList.add('wrong');
  });
  var fb = document.getElementById('storyFeedback');
  if (chosen === correct) {
    fb.style.display = 'block';
    fb.style.background = '#d4edda';
    fb.style.color = '#155724';
    fb.innerHTML = '\u2705 \u7b54\u5bf9\u4e86\uff01\u592d\u68d2\u4e86\uff01';
    addPoints(15);
  } else {
    fb.style.display = 'block';
    fb.style.background = '#f8d7da';
    fb.style.color = '#721c24';
    fb.innerHTML = '\u274c \u518d\u60f3\u60f3\uff1f\u6b63\u786e\u7b54\u6848\u662f ' + String.fromCharCode(65+correct);
  }
  updateGameStats();
}

function speakStory(title) {
  stopSpeak();
  var dayOfYear = Math.floor((Date.now() - new Date(new Date().getFullYear(),0,0)) / 86400000);
  var story = DAILY_STORIES[dayOfYear % DAILY_STORIES.length];
  var u = new SpeechSynthesisUtterance(story.t + '\u3002' + story.body);
  u.lang = 'zh-CN';
  u.rate = 0.75;
  u.pitch = 1.1;
  speechSynthesis.speak(u);
}

// ==================== GAME DICTATION ====================
var gameState = { level: 0, hearts: 3, correct: 0, wrong: 0, currentIdx: 0, items: [], levelStars: {} };

function getUnitLevels(unitNum) {
  var key = 'dict_levels_u' + unitNum;
  return JSON.parse(localStorage.getItem(key) || '{"0":0,"1":0,"2":0}');
}

function saveUnitLevels(unitNum, levels) {
  localStorage.setItem('dict_levels_u' + unitNum, JSON.stringify(levels));
}

function renderDictation() {
  var u = UNITS.find(function(x) { return x.num === currentUnit; });
  var words = u.review.words;
  var levels = getUnitLevels(currentUnit);
  var wordsPerLevel = 8;
  var totalLevels = Math.ceil(words.length / wordsPerLevel);
  
  var html = '<div class="unit active">';
  html += '<div class="unit-title">' + u.title + ' \xb7 \u95ef\u5173\u9ed8\u5199</div>';
  html += '<div class="unit-subtitle">\u9009\u62e9\u5173\u5361\u5f00\u59cb\u9ed8\u5199\uff0c\u6bcf\u51738\u4e2a\u5b57</div>';
  html += '<div class="level-grid">';
  for (var i = 0; i < totalLevels; i++) {
    var unlocked = i === 0 || levels[i-1] > 0;
    var completed = levels[i] > 0;
    var stars = levels[i] || 0;
    var starStr = '';
    for (var s = 0; s < 3; s++) starStr += s < stars ? '\u2b50' : '\u2606';
    html += '<div class="level-btn ' + (completed ? 'completed' : '') + (unlocked ? '' : 'locked') + '" ' + (unlocked ? 'onclick="startLevel(' + i + ')"' : '') + '>';
    html += '<div class="level-num">' + (i+1) + '</div>';
    html += '<div class="level-stars">' + starStr + '</div>';
    html += '</div>';
  }
  html += '</div></div>';
  document.getElementById('app').innerHTML = html;
}

function startLevel(level) {
  var u = UNITS.find(function(x) { return x.num === currentUnit; });
  var words = u.review.words;
  var start = level * 8;
  var end = Math.min(start + 8, words.length);
  gameState = { level: level, hearts: 3, correct: 0, wrong: 0, currentIdx: 0, items: [], levelStars: getUnitLevels(currentUnit) };
  gameState.items = [];
  for (var i = start; i < end; i++) {
    gameState.items.push({ id: 'g' + currentUnit + '-' + i, pinyin: words[i].pinyin, answer: words[i].char });
  }
  renderGameQuestion();
}

function renderGameQuestion() {
  var g = gameState;
  if (g.currentIdx >= g.items.length) { finishLevel(); return; }
  var item = g.items[g.currentIdx];
  var html = '<div class="unit active">';
  // Hearts
  html += '<div class="hearts">';
  for (var i = 0; i < 3; i++) html += '<span class="heart ' + (i < g.hearts ? '' : 'lost') + '">' + (i < g.hearts ? '\u2764\ufe0f' : '\u2764') + '</span>';
  html += '</div>';
  // Progress
  html += '<div style="text-align:center;color:var(--gray);font-size:0.9em;margin:8px 0">第 ' + (g.currentIdx+1) + ' / ' + g.items.length + ' \u9898</div>';
  // Question
  html += '<div class="game-question">';
  html += '<div class="game-pinyin">' + item.pinyin + '</div>';
  html += '<input class="game-input" id="gameInput" placeholder="\u8bf7\u8f93\u5165" autocomplete="off" autocapitalize="off">';
  html += '<div class="game-answer" id="gameAnswer" style="display:none"></div>';
  html += '</div>';
  html += '<div style="text-align:center;margin-top:16px"><button class="btn btn-primary" onclick="checkGameAnswer()">\u786e\u8ba4</button></div>';
  html += '</div>';
  document.getElementById('app').innerHTML = html;
  var inp = document.getElementById('gameInput');
  inp.focus();
  inp.addEventListener('keydown', function(e) { if (e.key === 'Enter') checkGameAnswer(); });
}

function checkGameAnswer() {
  var g = gameState;
  if (g.currentIdx >= g.items.length) return;
  var item = g.items[g.currentIdx];
  var inp = document.getElementById('gameInput');
  var ans = document.getElementById('gameAnswer');
  var val = inp.value.trim();
  if (!val) return;
  
  if (val === item.answer) {
    g.correct++;
    inp.classList.add('correct');
    ans.innerHTML = '<span class="correct-text">\u2705 \u7b54\u5bf9\u4e86\uff01</span>';
    addPoints(10);
    recordAnswer(item.id, true);
  } else {
    g.wrong++;
    g.hearts--;
    inp.classList.add('wrong');
    ans.innerHTML = '\u274c \u6b63\u786e\u7b54\u6848\uff1a<span class="correct-text">' + item.answer + '</span>';
    recordAnswer(item.id, false);
  }
  ans.style.display = 'block';
  inp.disabled = true;
  updateGameStats();
  
  setTimeout(function() {
    if (g.hearts <= 0) { gameOver(); return; }
    g.currentIdx++;
    renderGameQuestion();
  }, 1200);
}

function gameOver() {
  var html = '<div class="unit active">';
  html += '<div class="result-card">';
  html += '<div style="font-size:3em">\ud83d\ude22</div>';
  html += '<div class="result-text">\u751f\u547d\u7528\u5b8c\u4e86\uff01\u518d\u6765\u4e00\u6b21\u5427\uff01</div>';
  html += '<div class="btn-group" style="justify-content:center">';
  html += '<button class="btn btn-primary" onclick="startLevel(' + gameState.level + ')">\ud83d\udd04 \u91cd\u65b0\u5f00\u59cb</button>';
  html += '<button class="btn btn-blue" onclick="renderDictation()">\u2b05 \u8fd4\u56de</button>';
  html += '</div></div></div>';
  document.getElementById('app').innerHTML = html;
}

function finishLevel() {
  var g = gameState;
  var stars = g.wrong === 0 ? 3 : g.wrong <= 2 ? 2 : 1;
  var oldStars = g.levelStars[g.level] || 0;
  if (stars > oldStars) g.levelStars[g.level] = stars;
  saveUnitLevels(currentUnit, g.levelStars);
  addPoints(stars * 20);
  updateGameStats();
  
  var starStr = '';
  for (var i = 0; i < 3; i++) starStr += i < stars ? '\u2b50' : '\u2606';
  var html = '<div class="unit active">';
  html += '<div class="result-card">';
  html += '<div style="font-size:3em">\ud83c\udf89</div>';
  html += '<div class="result-stars">' + starStr + '</div>';
  html += '<div class="result-text">\u606d\u559c\u901a\u5173\uff01\u8d5f\u5f97 ' + (stars*20) + ' \u5206</div>';
  html += '<div style="color:var(--gray);font-size:0.9em">\u7b54\u5bf9 ' + g.correct + ' / ' + g.items.length + ' \u4e2a\uff0c\u9519\u8bef ' + g.wrong + ' \u4e2a</div>';
  html += '<div class="btn-group" style="justify-content:center;margin-top:16px">';
  var u = UNITS.find(function(x) { return x.num === currentUnit; });
  var totalLevels = Math.ceil(u.review.words.length / 8);
  if (g.level + 1 < totalLevels) {
    html += '<button class="btn btn-green" onclick="startLevel(' + (g.level+1) + ')">\u27a1 \u4e0b\u4e00\u5173</button>';
  }
  html += '<button class="btn btn-primary" onclick="renderDictation()">\ud83c\udfaf \u9009\u62e9\u5173\u5361</button>';
  html += '</div></div></div>';
  document.getElementById('app').innerHTML = html;
}
"""

content = content[:idx] + new_functions + content[idx:]

# === 4. Update switchMode and renderContent ===
content = content.replace(
    "case 'dictation': renderDictation(); break;",
    "case 'dictation': renderDictation(); break;\n    case 'recite': renderRecite(); break;\n    case 'story': renderStory(); break;"
)

# === 5. Remove dictation-hint CSS ===
content = content.replace('.dictation-hint{font-size:0.85em;color:var(--gray);margin-top:4px}\n', '')

with open(r'D:\语文复习App\docs\index.html', 'w', encoding='utf-8') as f:
    f.write(content)

print(f"File updated: {len(content)} chars")
