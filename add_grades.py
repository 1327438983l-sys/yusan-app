"""Add grade data to the app"""
with open(r'D:\语文复习App\docs\index.html', 'r', encoding='utf-8') as f:
    content = f.read()

# Find and replace switchGrade function
old_idx = content.find('function switchGrade(')
if old_idx < 0:
    print("ERROR: switchGrade not found")
    exit(1)

# Find the end of the function (next function definition)
end_markers = ['function loadGradeData', 'function switchSubject', '// =']
end_idx = len(content)
for marker in end_markers:
    idx = content.find(marker, old_idx + 10)
    if idx > 0 and idx < end_idx:
        end_idx = idx

# Also include the loadGradeData function if it exists
if 'function loadGradeData' in content[end_idx:end_idx+500]:
    ld_end = content.find('\nfunction ', end_idx + 20)
    if ld_end > end_idx:
        end_idx = ld_end

new_code = """var GRADE_DATA = {
  1: {
    vocab: [
      {lesson:'识字1',words:['一','二','三','四','五','六','七','八','九','十'],py:['yī','èr','sān','sì','wǔ','liù','qī','bā','jiǔ','shí']},
      {lesson:'识字2',words:['上','下','大','小','多','少','天','地','人','口'],py:['shàng','xià','dà','xiǎo','duō','shǎo','tiān','dì','rén','kǒu']},
      {lesson:'识字3',words:['日','月','水','火','山','石','田','土','目','耳'],py:['rì','yuè','shuǐ','huǒ','shān','shí','tián','tǔ','mù','ěr']},
      {lesson:'课文1',words:['爸','妈','马','土','不','八','入','大','天','人'],py:['bà','mā','mǎ','tǔ','bù','bā','rù','dà','tiān','rén']},
      {lesson:'课文2',words:['木','禾','竹','牙','尺','毛','卜','又','心','风'],py:['mù','hé','zhú','yá','chǐ','máo','bo','yòu','xīn','fēng']},
      {lesson:'课文3',words:['花','鸟','虫','牛','羊','小','少','多','果','瓜'],py:['huā','niǎo','chóng','niú','yáng','xiǎo','shǎo','duō','guǒ','guā']}
    ],
    math: [
      {unit:'数一数',formulas:['按顺序数数1-10'],practice:[{q:'3+2=?',a:'5'},{q:'7-3=?',a:'4'},{q:'2+6=?',a:'8'},{q:'9-4=?',a:'5'},{q:'4+4=?',a:'8'},{q:'10-6=?',a:'4'}]},
      {unit:'比一比',formulas:['多的画多少的画少'],practice:[{q:'5和3哪个大？',a:'5'},{q:'8和8一样大吗？',a:'一样'},{q:'4和7哪个小？',a:'4'},{q:'10和6哪个大？',a:'10'}]},
      {unit:'认识图形',formulas:['正方形四条边','三角形三条边','圆没有角'],practice:[{q:'正方形几条边？',a:'4'},{q:'三角形几条边？',a:'3'},{q:'长方形几条边？',a:'4'},{q:'圆有几个角？',a:'0'}]},
      {unit:'10以内加减法',formulas:['凑十法','破十法'],practice:[{q:'1+2=?',a:'3'},{q:'3+4=?',a:'7'},{q:'5+3=?',a:'8'},{q:'6+2=?',a:'8'},{q:'9-3=?',a:'6'},{q:'7-4=?',a:'3'},{q:'10-6=?',a:'4'},{q:'8-5=?',a:'3'}]}
    ]
  },
  2: {
    vocab: [
      {lesson:'识字1',words:['春','风','冬','雪','花','飞','入','姓','氏','李'],py:['chūn','fēng','dōng','xuě','huā','fēi','rù','xìng','shì','lǐ']},
      {lesson:'识字2',words:['张','吴','赵','钱','孙','周','王','方','国','全'],py:['zhāng','wú','zhào','qián','sūn','zhōu','wáng','fāng','guó','quán']},
      {lesson:'课文1',words:['清','晴','眼','睛','保','护','害','事','情','请'],py:['qīng','qíng','yǎn','jīng','bǎo','hù','hài','shì','qíng','qǐng']},
      {lesson:'课文2',words:['吃','叫','主','江','住','没','以','会','走','北'],py:['chī','jiào','zhǔ','jiāng','zhù','méi','yǐ','huì','zǒu','běi']},
      {lesson:'课文3',words:['会','走','北','京','门','广','公','厂'],py:['huì','zǒu','běi','jīng','mén','guǎng','gōng','chǎng']}
    ],
    math: [
      {unit:'100以内加减法',formulas:['相同数位对齐','从个位算起'],practice:[{q:'34+25=?',a:'59'},{q:'67+18=?',a:'85'},{q:'92-45=?',a:'47'},{q:'80-36=?',a:'44'},{q:'56+27=?',a:'83'},{q:'100-58=?',a:'42'}]},
      {unit:'乘法口诀',formulas:['一一得一到九九八十一'],practice:[{q:'3×4=?',a:'12'},{q:'5×6=?',a:'30'},{q:'7×8=?',a:'56'},{q:'9×9=?',a:'81'},{q:'4×7=?',a:'28'},{q:'6×6=?',a:'36'}]},
      {unit:'认识时间',formulas:['1小时=60分钟'],practice:[{q:'1小时=?分钟',a:'60'},{q:'钟面几个大格？',a:'12'},{q:'分针走一圈是？',a:'1小时'}]},
      {unit:'长度单位',formulas:['1米=100厘米'],practice:[{q:'1米=?厘米',a:'100'},{q:'3米=?厘米',a:'300'},{q:'500厘米=?米',a:'5'}]}
    ]
  },
  4: {
    vocab: [
      {lesson:'第一单元',words:['坪坝','穿戴','鲜艳','服装','打扮','朝霞','欢唱','招呼','飘扬','敬礼'],py:['píng bà','chuān dài','xiān yàn','fú zhuāng','dǎ bàn','zhāo xiá','huān chàng','zhāo hu','piāo yáng','jìng lǐ']},
      {lesson:'第二单元',words:['金色','石径','菊花','残阳','寒冷','盖','橙子','送别','挑水','萧萧'],py:['jīn sè','shí jìng','jú huā','cán yáng','hán lěng','gài','chéng zi','sòng bié','tiāo shuǐ','xiāo xiāo']},
      {lesson:'第三单元',words:['准备','墙壁','蜘蛛','漂亮','饱满','非常','独自','尽量'],py:['zhǔn bèi','qiáng bì','zhī zhū','piào liang','bǎo mǎn','fēi cháng','dú zì','jǐn liàng']},
      {lesson:'第四单元',words:['举世闻名','创举','冲毁','坚固','宝贵','遗产','设计','横跨'],py:['jǔ shì wén míng','chuàng jǔ','chōng huǐ','jiān gù','bǎo guì','yí chǎn','shè jì','héng kuà']}
    ],
    math: [
      {unit:'大数的认识',formulas:['个十百千万十万百万千万亿','每相邻单位进率是十'],practice:[{q:'一亿=?个万',a:'10000'},{q:'10个一千=?',a:'一万'},{q:'百万位是5表示？',a:'5个百万'},{q:'456789读作？',a:'四十五万六千七百八十九'},{q:'最大的四位数是？',a:'9999'},{q:'最小的五位数是？',a:'10000'}]},
      {unit:'三位数乘两位数',formulas:['先用个位乘再用十位乘最后相加'],practice:[{q:'123×45=?',a:'5535'},{q:'256×12=?',a:'3072'},{q:'345×20=?',a:'6900'},{q:'108×50=?',a:'5400'},{q:'234×11=?',a:'2574'},{q:'456×13=?',a:'5928'}]},
      {unit:'平行与垂直',formulas:['不相交的两条线平行','相交成直角垂直'],practice:[{q:'正方形相邻两边？',a:'垂直'},{q:'正方形对边？',a:'平行'},{q:'长方形几个直角？',a:'4'},{q:'平行线间距离？',a:'相等'}]}
    ]
  },
  5: {
    vocab: [
      {lesson:'第一单元',words:['精巧','色素','配合','身段','生硬','寻常','忘却','结构','镜匣','清晨'],py:['jīng qiǎo','sè sǔn','pèi hé','shēn duàn','shēng yìng','xún cháng','wàng què','jié gòu','jìng xiá','qīng chén']},
      {lesson:'第二单元',words:['猎豹','陆地','俯冲','搭乘','火箭','发动机','手电筒','赤道','难以置信','呼啸'],py:['liè bào','lù dì','fǔ chōng','dā chéng','huǒ jiàn','fā dòng jī','shǒu diàn tǒng','chì dào','nán yǐ zhì xìn','hū xiào']},
      {lesson:'第三单元',words:['汛期','谴责','懒惰','平稳','平衡','协调','山洪','暴发','间隔','联结'],py:['xùn qī','qiǎn zé','lǎn duò','píng wěn','píng héng','xié tiáo','shān hóng','bào fā','jiàn gé','lián jié']},
      {lesson:'第四单元',words:['甚至','顽皮','极了','注视','静寂','站岗','理睬','无疑','歇息','偶尔'],py:['shèn zhì','wán pí','jí le','zhù shì','jìng jì','zhàn gǎng','lǐ cǎi','wú yí','xiē xī','ǒu ěr']}
    ],
    math: [
      {unit:'小数乘法',formulas:['先按整数乘再点小数点'],practice:[{q:'2.5×4=?',a:'10'},{q:'1.2×3=?',a:'3.6'},{q:'0.8×0.5=?',a:'0.4'},{q:'3.6×0.2=?',a:'0.72'},{q:'1.5×0.6=?',a:'0.9'},{q:'4.5×0.4=?',a:'1.8'}]},
      {unit:'简易方程',formulas:['含有未知数的等式叫方程','解方程用等式性质'],practice:[{q:'x+5=12,x=?',a:'7'},{q:'3x=18,x=?',a:'6'},{q:'x-7=3,x=?',a:'10'},{q:'2x+4=10,x=?',a:'3'},{q:'5x-3=12,x=?',a:'3'},{q:'x/4=5,x=?',a:'20'}]},
      {unit:'多边形面积',formulas:['平行四边形=底×高','三角形=底×高÷2','梯形=(上底+下底)×高÷2'],practice:[{q:'底5高3平行四边形=?',a:'15'},{q:'底6高4三角形=?',a:'12'},{q:'上底3下底7高4梯形=?',a:'20'},{q:'底8高5平行四边形=?',a:'40'},{q:'底10高6三角形=?',a:'30'},{q:'上底2下底8高5梯形=?',a:'25'}]}
    ]
  },
  6: {
    vocab: [
      {lesson:'第一单元',words:['绿毯','线条','柔美','惊叹','回味','乐趣','目的地','洒脱','衣裳','彩虹'],py:['lǜ tǎn','xiàn tiáo','róu měi','jīng tàn','huí wèi','lè qù','mù dì dì','sǎ tuō','yī shang','cǎi hóng']},
      {lesson:'第二单元',words:['日寇','奋战','壮烈','豪迈','不屈','悬崖','斩钉截铁','热血沸腾','居高临下','粉身碎骨'],py:['rì kòu','fèn zhàn','zhuàng liè','háo mài','bù qū','xuán yá','zhǎn dīng jié tiě','rè xuè fèi téng','jū gāo lín xià','fěn shēn suì gǔ']},
      {lesson:'第三单元',words:['竹节人','威风凛凛','疙瘩','疲倦','冰棍','别出心裁','技高一筹','大步流星','忘乎所以','心满意足'],py:['zhú jié rén','wēi fēng lǐn lǐn','gē da','pí juàn','bīng gùn','bié chū xīn cái','jì gāo yī chóu','dà bù liú xīng','wàng huū suǒ yǐ','xīn mǎn yì zú']},
      {lesson:'第四单元',words:['咆哮','惊慌','拥戴','沙哑','呻吟','放肆','搀扶','势不可当','跌跌撞撞','你拥我挤'],py:['páo xiào','jīng huāng','yōng dài','shā yǎ','shēn yín','fàng sì','chān fú','shì bù kě dāng','diē diē zhuàng zhuàng','nǐ yōng wǒ jǐ']}
    ],
    math: [
      {unit:'分数乘法',formulas:['分子×整数/分母','分子相乘/分母相乘','结果约分'],practice:[{q:'1/2×3=?',a:'3/2'},{q:'2/3×4=?',a:'8/3'},{q:'1/4×2/3=?',a:'2/12'},{q:'3/5×5/6=?',a:'1/2'},{q:'2/7×3=?',a:'6/7'},{q:'5/8×4/5=?',a:'1/2'}]},
      {unit:'百分数',formulas:['小数→%: ×100加%','分数→%: 分子÷分母×100'],practice:[{q:'0.75=?%',a:'75%'},{q:'3/4=?%',a:'75%'},{q:'40%=?小数',a:'0.4'},{q:'60%=?分数',a:'3/5'},{q:'2/5=?%',a:'40%'},{q:'0.25=?%',a:'25%'}]},
      {unit:'圆的面积',formulas:['面积=πr²','周长=2πr=πd','π≈3.14'],practice:[{q:'r=3cm面积=?',a:'28.26'},{q:'d=10cm周长=?',a:'31.4'},{q:'r=5cm面积=?',a:'78.5'},{q:'r=2cm面积=?',a:'12.56'},{q:'d=8cm周长=?',a:'25.12'},{q:'r=4cm面积=?',a:'50.24'}]}
    ]
  }
};

var currentGrade = parseInt(localStorage.getItem('app_grade') || '3');

function switchGrade(grade) {
  currentGrade = grade;
  localStorage.setItem('app_grade', grade);
  document.querySelectorAll('.grade-btn').forEach(function(b, i) {
    b.classList.toggle('active', i + 1 === grade);
  });
  var engBtn = document.querySelector('.subject-btn[data-subj="english"]');
  if (engBtn) engBtn.style.display = grade <= 2 ? 'none' : '';
  if (currentSubject === 'english' && grade <= 2) switchSubject('chinese');
  var titles = {1:'一年级',2:'二年级',3:'三年级',4:'四年级',5:'五年级',6:'六年级'};
  var el = document.getElementById('appTitle');
  if (el) el.textContent = titles[grade] + '下册';
  // Load grade data
  var d = GRADE_DATA[grade];
  if (d) {
    if (d.vocab) TEXTBOOK_VOCAB = d.vocab;
    if (d.math) MATH_UNITS = d.math;
    if (d.english) ENGLISH_UNITS = d.english;
  }
  currentUnit = 1;
  renderModeTabs();
  renderUnitTabs();
  renderContent();
  scrollToTop();
}
"""

content = content[:old_idx] + new_code + content[end_idx:]

with open(r'D:\语文复习App\docs\index.html', 'w', encoding='utf-8') as f:
    f.write(content)

# Verify
import subprocess
result = subprocess.run(['node', '-e', r'''
const fs = require("fs");
const html = fs.readFileSync("D:/语文复习App/docs/index.html", "utf8");
const m = html.match(/<script>([\s\S]*?)<\/script>/);
if (m) {
  try { new Function(m[1]); console.log("SYNTAX OK"); }
  catch(e) { console.log("ERR:", e.message.substring(0,200)); }
}
'''], capture_output=True, text=True, timeout=10)
print(result.stdout.strip())
print(f"File: {len(content)} chars")
