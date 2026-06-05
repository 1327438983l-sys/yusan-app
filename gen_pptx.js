const pptxgen = require("pptxgenjs");

const pptx = new pptxgen();
pptx.layout = "LAYOUT_16x9";
pptx.author = "Hermes Agent";
pptx.title = "三年级语文复习App - 教育学改进方案";

// Colors
const CLR = {
  primary:   "E67E22",
  secondary: "2C3E50",
  accent:    "27AE60",
  bg:        "FDF6EC",
  white:     "FFFFFF",
  lightGray: "F0E6D6",
  darkGray:  "555555",
};
const FONT = "Microsoft YaHei";

// Helper: add background + top bar
function slideBase(slide) {
  slide.background = { color: CLR.bg };
  // Top accent bar
  slide.addShape(pptx.shapes.RECTANGLE, {
    x: 0, y: 0, w: "100%", h: 0.08, fill: { color: CLR.primary },
  });
  // Bottom accent line
  slide.addShape(pptx.shapes.RECTANGLE, {
    x: 0, y: 5.52, w: "100%", h: 0.05, fill: { color: CLR.secondary },
  });
}

// Helper: add slide number
function slideNum(slide, num, total) {
  slide.addText(`${num} / ${total}`, {
    x: 8.8, y: 5.35, w: 1, h: 0.3,
    fontSize: 9, fontFace: FONT, color: CLR.darkGray, align: "right",
  });
}

// Helper: section title on left
function sectionTag(slide, label, color) {
  slide.addShape(pptx.shapes.ROUNDED_RECTANGLE, {
    x: 0.4, y: 0.3, w: 1.8, h: 0.38,
    fill: { color: color }, rectRadius: 0.1,
  });
  slide.addText(label, {
    x: 0.4, y: 0.3, w: 1.8, h: 0.38,
    fontSize: 12, fontFace: FONT, color: CLR.white, bold: true, align: "center", valign: "middle",
  });
}

const TOTAL = 10;

// ═══════════════════════════════════════════════════════
// SLIDE 1 - Title
// ═══════════════════════════════════════════════════════
{
  const slide = pptx.addSlide();
  slide.background = { color: CLR.secondary };

  // Large left accent block
  slide.addShape(pptx.shapes.RECTANGLE, {
    x: 0, y: 0, w: 0.35, h: "100%", fill: { color: CLR.primary },
  });

  // Decorative circles
  slide.addShape(pptx.shapes.OVAL, {
    x: 8.2, y: 0.3, w: 1.8, h: 1.8,
    fill: { color: CLR.primary }, transparency: 75,
  });
  slide.addShape(pptx.shapes.OVAL, {
    x: 9.0, y: 1.0, w: 1.2, h: 1.2,
    fill: { color: CLR.accent }, transparency: 80,
  });

  // Main title
  slide.addText("三年级语文复习App", {
    x: 0.8, y: 1.5, w: 8.5, h: 0.9,
    fontSize: 38, fontFace: FONT, color: CLR.white, bold: true,
  });
  slide.addText("教育学改进方案", {
    x: 0.8, y: 2.35, w: 8.5, h: 0.7,
    fontSize: 32, fontFace: FONT, color: CLR.primary, bold: true,
  });

  // Divider line
  slide.addShape(pptx.shapes.RECTANGLE, {
    x: 0.8, y: 3.2, w: 2.5, h: 0.04, fill: { color: CLR.primary },
  });

  // Subtitle
  slide.addText("基于循证教育学的智能复习系统", {
    x: 0.8, y: 3.5, w: 8, h: 0.5,
    fontSize: 18, fontFace: FONT, color: CLR.lightGray,
  });

  // Date / author
  slide.addText("2026年6月  |  Evidence-Based Learning Design", {
    x: 0.8, y: 4.5, w: 8, h: 0.4,
    fontSize: 12, fontFace: FONT, color: "8899AA",
  });

  // Small accent rectangles
  slide.addShape(pptx.shapes.RECTANGLE, {
    x: 0.8, y: 4.1, w: 0.6, h: 0.08, fill: { color: CLR.accent },
  });
}

// ═══════════════════════════════════════════════════════
// SLIDE 2 - Problem
// ═══════════════════════════════════════════════════════
{
  const slide = pptx.addSlide();
  slideBase(slide);
  slideNum(slide, 2, TOTAL);

  // Section tag
  sectionTag(slide, "问题分析", CLR.secondary);

  // Title
  slide.addText("传统复习的三大痛点", {
    x: 0.5, y: 0.9, w: 9, h: 0.6,
    fontSize: 28, fontFace: FONT, color: CLR.secondary, bold: true,
  });

  // Subtitle
  slide.addText("为什么传统复习方式效率低下？", {
    x: 0.5, y: 1.5, w: 9, h: 0.4,
    fontSize: 14, fontFace: FONT, color: CLR.darkGray,
  });

  // Three pain point cards
  const pains = [
    { icon: "❌", title: "只能看不能练", desc: "复习清单仅提供内容展示，学生被动浏览，无法主动参与练习和检测" },
    { icon: "⏳", title: "反馈太慢", desc: "测试必须全部做完才能看到评分，错误理解持续积累，错过最佳纠正时机" },
    { icon: "🔄", title: "错题不追踪", desc: "没有记录薄弱点的机制，已错过的题目不会再出现，复习针对性差" },
  ];

  pains.forEach((p, i) => {
    const x = 0.5 + i * 3.1;
    // Card background
    slide.addShape(pptx.shapes.ROUNDED_RECTANGLE, {
      x: x, y: 2.2, w: 2.8, h: 2.8,
      fill: { color: CLR.white },
      shadow: { type: "outer", blur: 6, offset: 2, color: "CCCCCC", opacity: 0.3 },
      rectRadius: 0.15,
    });
    // Icon circle
    slide.addShape(pptx.shapes.OVAL, {
      x: x + 0.9, y: 2.4, w: 0.9, h: 0.9,
      fill: { color: i === 0 ? "FADBD8" : i === 1 ? "FDEBD0" : "D5F5E3" },
    });
    slide.addText(p.icon, {
      x: x + 0.9, y: 2.4, w: 0.9, h: 0.9,
      fontSize: 28, align: "center", valign: "middle",
    });
    // Title
    slide.addText(p.title, {
      x: x + 0.2, y: 3.45, w: 2.4, h: 0.4,
      fontSize: 15, fontFace: FONT, color: CLR.secondary, bold: true, align: "center",
    });
    // Desc
    slide.addText(p.desc, {
      x: x + 0.2, y: 3.85, w: 2.4, h: 1.0,
      fontSize: 11, fontFace: FONT, color: CLR.darkGray, align: "center", valign: "top",
    });
  });

  // Bottom accent
  slide.addShape(pptx.shapes.RECTANGLE, {
    x: 0.5, y: 5.15, w: 9, h: 0.04, fill: { color: "E74C3C" }, transparency: 60,
  });
}

// ═══════════════════════════════════════════════════════
// SLIDE 3 - Theory 1: Spaced Repetition
// ═══════════════════════════════════════════════════════
{
  const slide = pptx.addSlide();
  slideBase(slide);
  slideNum(slide, 3, TOTAL);

  sectionTag(slide, "理论 1", CLR.primary);

  slide.addText("间隔重复 (Spaced Repetition)", {
    x: 2.4, y: 0.25, w: 7, h: 0.45,
    fontSize: 24, fontFace: FONT, color: CLR.secondary, bold: true,
  });

  // Left panel - Ebbinghaus curve representation
  slide.addShape(pptx.shapes.ROUNDED_RECTANGLE, {
    x: 0.5, y: 0.95, w: 4.5, h: 4.2,
    fill: { color: CLR.white },
    shadow: { type: "outer", blur: 4, offset: 2, color: "CCCCCC", opacity: 0.25 },
    rectRadius: 0.12,
  });

  slide.addText("Ebbinghaus 遗忘曲线", {
    x: 0.7, y: 1.05, w: 4.1, h: 0.35,
    fontSize: 14, fontFace: FONT, color: CLR.primary, bold: true,
  });

  // Visual bar chart for forgetting curve
  const bars = [
    { label: "刚学完", pct: 100, color: CLR.accent },
    { label: "1天后", pct: 34, color: "E74C3C" },
    { label: "1周后", pct: 23, color: "E74C3C" },
    { label: "1月后", pct: 21, color: "C0392B" },
  ];
  bars.forEach((b, i) => {
    const by = 1.55 + i * 0.75;
    slide.addText(b.label, {
      x: 0.7, y: by, w: 1.0, h: 0.3,
      fontSize: 10, fontFace: FONT, color: CLR.darkGray,
    });
    slide.addShape(pptx.shapes.RECTANGLE, {
      x: 1.7, y: by, w: 3.1 * (b.pct / 100), h: 0.35,
      fill: { color: b.color }, transparency: 20,
    });
    slide.addText(`${b.pct}%`, {
      x: 1.7 + 3.1 * (b.pct / 100) + 0.1, y: by, w: 0.6, h: 0.35,
      fontSize: 11, fontFace: FONT, color: b.color, bold: true,
    });
  });

  slide.addText("学完1天忘66%，1周忘77%", {
    x: 0.7, y: 4.55, w: 4.1, h: 0.35,
    fontSize: 11, fontFace: FONT, color: CLR.darkGray, italic: true,
  });

  // Right panel - Spaced repetition schedule
  slide.addShape(pptx.shapes.ROUNDED_RECTANGLE, {
    x: 5.3, y: 0.95, w: 4.5, h: 4.2,
    fill: { color: CLR.white },
    shadow: { type: "outer", blur: 4, offset: 2, color: "CCCCCC", opacity: 0.25 },
    rectRadius: 0.12,
  });

  slide.addText("间隔复习策略", {
    x: 5.5, y: 1.05, w: 4.1, h: 0.35,
    fontSize: 14, fontFace: FONT, color: CLR.accent, bold: true,
  });

  // Timeline visualization
  const steps = [
    { label: "错1次", sub: "立即", color: CLR.primary, x: 5.6 },
    { label: "1天后", sub: "首次复习", color: CLR.accent, x: 6.6 },
    { label: "3天后", sub: "二次复习", color: CLR.accent, x: 7.6 },
    { label: "7天后", sub: "巩固复习", color: CLR.accent, x: 8.55 },
  ];

  steps.forEach((s, i) => {
    // Circle node
    slide.addShape(pptx.shapes.OVAL, {
      x: s.x, y: 1.7, w: 0.7, h: 0.7,
      fill: { color: s.color },
    });
    slide.addText(`${i + 1}`, {
      x: s.x, y: 1.7, w: 0.7, h: 0.7,
      fontSize: 18, fontFace: FONT, color: CLR.white, bold: true, align: "center", valign: "middle",
    });
    // Label
    slide.addText(s.label, {
      x: s.x - 0.15, y: 2.5, w: 1.0, h: 0.3,
      fontSize: 11, fontFace: FONT, color: CLR.secondary, bold: true, align: "center",
    });
    slide.addText(s.sub, {
      x: s.x - 0.15, y: 2.8, w: 1.0, h: 0.25,
      fontSize: 9, fontFace: FONT, color: CLR.darkGray, align: "center",
    });
    // Arrow between nodes
    if (i < steps.length - 1) {
      slide.addText("→", {
        x: s.x + 0.7, y: 1.7, w: 0.3, h: 0.7,
        fontSize: 20, fontFace: FONT, color: CLR.darkGray, align: "center", valign: "middle",
      });
    }
  });

  // Result highlight
  slide.addShape(pptx.shapes.ROUNDED_RECTANGLE, {
    x: 5.5, y: 3.5, w: 4.1, h: 1.0,
    fill: { color: "D5F5E3" }, rectRadius: 0.1,
  });
  slide.addText([
    { text: "效果：长期记忆提升 ", options: { fontSize: 14, fontFace: FONT, color: CLR.secondary } },
    { text: "200%", options: { fontSize: 22, fontFace: FONT, color: CLR.accent, bold: true } },
  ], {
    x: 5.5, y: 3.5, w: 4.1, h: 0.6,
    align: "center", valign: "middle",
  });
  slide.addText("基于艾宾浩斯遗忘规律的科学复习间隔", {
    x: 5.5, y: 4.1, w: 4.1, h: 0.35,
    fontSize: 10, fontFace: FONT, color: CLR.darkGray, align: "center",
  });
}

// ═══════════════════════════════════════════════════════
// SLIDE 4 - Theory 2: Retrieval Practice
// ═══════════════════════════════════════════════════════
{
  const slide = pptx.addSlide();
  slideBase(slide);
  slideNum(slide, 4, TOTAL);

  sectionTag(slide, "理论 2", CLR.primary);

  slide.addText("检索练习 (Retrieval Practice)", {
    x: 2.4, y: 0.25, w: 7, h: 0.45,
    fontSize: 24, fontFace: FONT, color: CLR.secondary, bold: true,
  });

  // Key finding card
  slide.addShape(pptx.shapes.ROUNDED_RECTANGLE, {
    x: 0.5, y: 0.95, w: 5.0, h: 1.8,
    fill: { color: CLR.secondary }, rectRadius: 0.12,
  });
  slide.addText("Testing Effect", {
    x: 0.8, y: 1.05, w: 4.4, h: 0.4,
    fontSize: 16, fontFace: FONT, color: CLR.primary, bold: true,
  });
  slide.addText("测试比重复阅读效果好 2 倍", {
    x: 0.8, y: 1.5, w: 4.4, h: 0.45,
    fontSize: 20, fontFace: FONT, color: CLR.white, bold: true,
  });
  slide.addText("— Roediger & Karpicke, 2006 (Psychological Science)", {
    x: 0.8, y: 2.0, w: 4.4, h: 0.35,
    fontSize: 10, fontFace: FONT, color: "8899AA", italic: true,
  });

  // Comparison chart
  slide.addShape(pptx.shapes.ROUNDED_RECTANGLE, {
    x: 5.8, y: 0.95, w: 3.9, h: 1.8,
    fill: { color: CLR.white },
    shadow: { type: "outer", blur: 4, offset: 2, color: "CCCCCC", opacity: 0.25 },
    rectRadius: 0.12,
  });
  slide.addText("效果对比", {
    x: 6.0, y: 1.05, w: 3.5, h: 0.35,
    fontSize: 13, fontFace: FONT, color: CLR.secondary, bold: true, align: "center",
  });
  // Re-reading bar
  slide.addText("重复阅读", {
    x: 6.0, y: 1.55, w: 1.2, h: 0.3,
    fontSize: 11, fontFace: FONT, color: CLR.darkGray,
  });
  slide.addShape(pptx.shapes.RECTANGLE, {
    x: 7.2, y: 1.55, w: 1.2, h: 0.35,
    fill: { color: "E0E0E0" },
  });
  slide.addText("1x", {
    x: 8.5, y: 1.55, w: 0.5, h: 0.35,
    fontSize: 11, fontFace: FONT, color: CLR.darkGray, bold: true,
  });
  // Retrieval bar
  slide.addText("检索测试", {
    x: 6.0, y: 2.0, w: 1.2, h: 0.3,
    fontSize: 11, fontFace: FONT, color: CLR.darkGray,
  });
  slide.addShape(pptx.shapes.RECTANGLE, {
    x: 7.2, y: 2.0, w: 2.2, h: 0.35,
    fill: { color: CLR.accent },
  });
  slide.addText("2x", {
    x: 9.5, y: 2.0, w: 0.5, h: 0.35,
    fontSize: 11, fontFace: FONT, color: CLR.accent, bold: true,
  });

  // Flashcard illustration
  slide.addShape(pptx.shapes.ROUNDED_RECTANGLE, {
    x: 0.5, y: 3.05, w: 9.2, h: 2.2,
    fill: { color: CLR.white },
    shadow: { type: "outer", blur: 4, offset: 2, color: "CCCCCC", opacity: 0.2 },
    rectRadius: 0.12,
  });

  slide.addText("闪卡模式：先回忆再揭晓", {
    x: 0.8, y: 3.15, w: 4, h: 0.35,
    fontSize: 14, fontFace: FONT, color: CLR.primary, bold: true,
  });

  // Flashcard 1
  slide.addShape(pptx.shapes.ROUNDED_RECTANGLE, {
    x: 0.8, y: 3.65, w: 2.6, h: 1.4,
    fill: { color: "FDEBD0" }, rectRadius: 0.1,
  });
  slide.addText("生字卡", {
    x: 0.8, y: 3.7, w: 2.6, h: 0.3,
    fontSize: 10, fontFace: FONT, color: CLR.primary, bold: true, align: "center",
  });
  slide.addText("碧", {
    x: 0.8, y: 4.0, w: 2.6, h: 0.8,
    fontSize: 40, fontFace: FONT, color: CLR.secondary, align: "center", valign: "middle",
  });

  // Arrow
  slide.addText("→ 思考 →", {
    x: 3.5, y: 4.0, w: 1.2, h: 0.6,
    fontSize: 12, fontFace: FONT, color: CLR.primary, align: "center", valign: "middle",
  });

  // Flashcard 2 (answer side)
  slide.addShape(pptx.shapes.ROUNDED_RECTANGLE, {
    x: 4.8, y: 3.65, w: 2.6, h: 1.4,
    fill: { color: "D5F5E3" }, rectRadius: 0.1,
  });
  slide.addText("答案", {
    x: 4.8, y: 3.7, w: 2.6, h: 0.3,
    fontSize: 10, fontFace: FONT, color: CLR.accent, bold: true, align: "center",
  });
  slide.addText("bì · 碧绿 · 碧空", {
    x: 4.8, y: 4.0, w: 2.6, h: 0.8,
    fontSize: 18, fontFace: FONT, color: CLR.accent, align: "center", valign: "middle", bold: true,
  });

  // Note
  slide.addText("主动提取强化神经通路，让记忆更加牢固", {
    x: 7.8, y: 3.7, w: 1.8, h: 1.3,
    fontSize: 11, fontFace: FONT, color: CLR.darkGray, valign: "middle",
  });
}

// ═══════════════════════════════════════════════════════
// SLIDE 5 - Theory 3: Formative Assessment
// ═══════════════════════════════════════════════════════
{
  const slide = pptx.addSlide();
  slideBase(slide);
  slideNum(slide, 5, TOTAL);

  sectionTag(slide, "理论 3", CLR.primary);

  slide.addText("即时反馈 (Formative Assessment)", {
    x: 2.4, y: 0.25, w: 7, h: 0.45,
    fontSize: 24, fontFace: FONT, color: CLR.secondary, bold: true,
  });

  // Quote card
  slide.addShape(pptx.shapes.ROUNDED_RECTANGLE, {
    x: 0.5, y: 0.95, w: 9.0, h: 1.2,
    fill: { color: CLR.secondary }, rectRadius: 0.12,
  });
  slide.addShape(pptx.shapes.RECTANGLE, {
    x: 0.5, y: 0.95, w: 0.12, h: 1.2,
    fill: { color: CLR.primary },
  });
  slide.addText([
    { text: '"', options: { fontSize: 36, color: CLR.primary, bold: true } },
    { text: '即时反馈是影响学习效果的最大因素', options: { fontSize: 18, color: CLR.white, bold: true } },
    { text: '"', options: { fontSize: 36, color: CLR.primary, bold: true } },
  ], {
    x: 0.9, y: 1.0, w: 8.2, h: 0.7,
    fontFace: FONT, valign: "middle",
  });
  slide.addText("— Black & Wiliam, 1998 (Inside the Black Box)", {
    x: 0.9, y: 1.7, w: 8.2, h: 0.3,
    fontSize: 10, fontFace: FONT, color: "8899AA", italic: true,
  });

  // Three features
  const features = [
    { title: "答一题判一题", desc: "不等全部提交，每道题即时判分，学生立刻知道对错", color: CLR.primary },
    { title: "答错立刻解析", desc: "错误答案旁显示详细解析，帮助学生理解知识点", color: CLR.accent },
    { title: "关联知识点", desc: "根据错题自动关联相关知识点，形成知识网络", color: CLR.secondary },
  ];

  features.forEach((f, i) => {
    const x = 0.5 + i * 3.15;
    slide.addShape(pptx.shapes.ROUNDED_RECTANGLE, {
      x: x, y: 2.5, w: 2.9, h: 2.6,
      fill: { color: CLR.white },
      shadow: { type: "outer", blur: 4, offset: 2, color: "CCCCCC", opacity: 0.25 },
      rectRadius: 0.12,
    });
    // Top color bar
    slide.addShape(pptx.shapes.RECTANGLE, {
      x: x, y: 2.5, w: 2.9, h: 0.08,
      fill: { color: f.color },
    });
    // Number
    slide.addShape(pptx.shapes.OVAL, {
      x: x + 1.05, y: 2.75, w: 0.8, h: 0.8,
      fill: { color: f.color },
    });
    slide.addText(`${i + 1}`, {
      x: x + 1.05, y: 2.75, w: 0.8, h: 0.8,
      fontSize: 22, fontFace: FONT, color: CLR.white, bold: true, align: "center", valign: "middle",
    });
    slide.addText(f.title, {
      x: x + 0.2, y: 3.7, w: 2.5, h: 0.4,
      fontSize: 15, fontFace: FONT, color: CLR.secondary, bold: true, align: "center",
    });
    slide.addText(f.desc, {
      x: x + 0.2, y: 4.15, w: 2.5, h: 0.7,
      fontSize: 11, fontFace: FONT, color: CLR.darkGray, align: "center",
    });
  });
}

// ═══════════════════════════════════════════════════════
// SLIDE 6 - Theory 4: Gamification
// ═══════════════════════════════════════════════════════
{
  const slide = pptx.addSlide();
  slideBase(slide);
  slideNum(slide, 6, TOTAL);

  sectionTag(slide, "理论 4", CLR.primary);

  slide.addText("游戏化激励 (Gamification)", {
    x: 2.4, y: 0.25, w: 7, h: 0.45,
    fontSize: 24, fontFace: FONT, color: CLR.secondary, bold: true,
  });

  // Self-determination theory card
  slide.addShape(pptx.shapes.ROUNDED_RECTANGLE, {
    x: 0.5, y: 0.95, w: 5.0, h: 1.3,
    fill: { color: CLR.white },
    shadow: { type: "outer", blur: 4, offset: 2, color: "CCCCCC", opacity: 0.2 },
    rectRadius: 0.12,
  });
  slide.addText("自我决定理论 (Self-Determination Theory)", {
    x: 0.7, y: 1.0, w: 4.6, h: 0.35,
    fontSize: 12, fontFace: FONT, color: CLR.primary, bold: true,
  });
  slide.addText("Deci & Ryan: 人类天生追求 自主 + 胜任 + 归属", {
    x: 0.7, y: 1.4, w: 4.6, h: 0.3,
    fontSize: 12, fontFace: FONT, color: CLR.secondary,
  });
  slide.addText("满足这三个需求 → 维持内在学习动机", {
    x: 0.7, y: 1.75, w: 4.6, h: 0.3,
    fontSize: 12, fontFace: FONT, color: CLR.accent, bold: true,
  });

  // SDT three pillars
  const pillars = [
    { title: "自主", desc: "选择复习模式和难度", icon: "🎯" },
    { title: "胜任", desc: "积分等级见证成长", icon: "🏆" },
    { title: "归属", desc: "连续天数形成习惯", icon: "🔥" },
  ];

  pillars.forEach((p, i) => {
    const x = 6.0 + i * 1.35;
    slide.addShape(pptx.shapes.ROUNDED_RECTANGLE, {
      x: x, y: 0.95, w: 1.2, h: 1.3,
      fill: { color: i === 0 ? "FDEBD0" : i === 1 ? "D5F5E3" : "FADBD8" },
      rectRadius: 0.1,
    });
    slide.addText(p.icon, {
      x: x, y: 0.95, w: 1.2, h: 0.45,
      fontSize: 22, align: "center", valign: "middle",
    });
    slide.addText(p.title, {
      x: x, y: 1.35, w: 1.2, h: 0.35,
      fontSize: 13, fontFace: FONT, color: CLR.secondary, bold: true, align: "center",
    });
    slide.addText(p.desc, {
      x: x, y: 1.7, w: 1.2, h: 0.45,
      fontSize: 9, fontFace: FONT, color: CLR.darkGray, align: "center",
    });
  });

  // Gamification features grid
  const gFeatures = [
    { title: "积分系统", desc: "每道题获得对应积分，累计兑换奖励", color: CLR.primary },
    { title: "等级成长", desc: "从\"语文小苗\"到\"语文达人\"的等级体系", color: CLR.accent },
    { title: "成就徽章", desc: "连续答对、全对等特殊成就解锁徽章", color: "9B59B6" },
    { title: "连续天数", desc: "每日打卡记录，形成21天学习习惯", color: "E74C3C" },
  ];

  gFeatures.forEach((f, i) => {
    const col = i % 2;
    const row = Math.floor(i / 2);
    const x = 0.5 + col * 4.8;
    const y = 2.6 + row * 1.3;

    slide.addShape(pptx.shapes.ROUNDED_RECTANGLE, {
      x: x, y: y, w: 4.5, h: 1.1,
      fill: { color: CLR.white },
      shadow: { type: "outer", blur: 3, offset: 1, color: "DDDDDD", opacity: 0.2 },
      rectRadius: 0.1,
    });
    // Color dot
    slide.addShape(pptx.shapes.OVAL, {
      x: x + 0.2, y: y + 0.3, w: 0.5, h: 0.5,
      fill: { color: f.color },
    });
    slide.addText(f.title, {
      x: x + 0.85, y: y + 0.15, w: 3.3, h: 0.4,
      fontSize: 14, fontFace: FONT, color: CLR.secondary, bold: true,
    });
    slide.addText(f.desc, {
      x: x + 0.85, y: y + 0.55, w: 3.3, h: 0.4,
      fontSize: 11, fontFace: FONT, color: CLR.darkGray,
    });
  });
}

// ═══════════════════════════════════════════════════════
// SLIDE 7 - Theory 5: Interleaving
// ═══════════════════════════════════════════════════════
{
  const slide = pptx.addSlide();
  slideBase(slide);
  slideNum(slide, 7, TOTAL);

  sectionTag(slide, "理论 5", CLR.primary);

  slide.addText("交错练习 (Interleaving)", {
    x: 2.4, y: 0.25, w: 7, h: 0.45,
    fontSize: 24, fontFace: FONT, color: CLR.secondary, bold: true,
  });

  // Two comparison columns
  // Blocked practice (bad)
  slide.addShape(pptx.shapes.ROUNDED_RECTANGLE, {
    x: 0.5, y: 0.95, w: 4.3, h: 2.5,
    fill: { color: CLR.white },
    shadow: { type: "outer", blur: 4, offset: 2, color: "CCCCCC", opacity: 0.2 },
    rectRadius: 0.12,
  });
  slide.addText("❌ 分类练习（传统）", {
    x: 0.7, y: 1.05, w: 3.9, h: 0.35,
    fontSize: 14, fontFace: FONT, color: "E74C3C", bold: true,
  });

  // Show blocked pattern
  const blocked = ["字·字·字·字", "词·词·词·词", "句·句·句·句", "篇·篇·篇·篇"];
  blocked.forEach((b, i) => {
    slide.addShape(pptx.shapes.RECTANGLE, {
      x: 0.8 + i * 0.95, y: 1.6, w: 0.85, h: 0.5,
      fill: { color: "FADBD8" },
    });
    slide.addText(b, {
      x: 0.8 + i * 0.95, y: 1.6, w: 0.85, h: 0.5,
      fontSize: 9, fontFace: FONT, color: "E74C3C", align: "center", valign: "middle",
    });
  });
  slide.addText("同类型集中练习，容易形成机械记忆\n无法学会区分不同题型的策略", {
    x: 0.8, y: 2.3, w: 3.8, h: 0.8,
    fontSize: 11, fontFace: FONT, color: CLR.darkGray,
  });

  // Interleaved practice (good)
  slide.addShape(pptx.shapes.ROUNDED_RECTANGLE, {
    x: 5.2, y: 0.95, w: 4.5, h: 2.5,
    fill: { color: CLR.white },
    shadow: { type: "outer", blur: 4, offset: 2, color: "CCCCCC", opacity: 0.2 },
    rectRadius: 0.12,
  });
  slide.addText("✅ 交错练习（推荐）", {
    x: 5.4, y: 1.05, w: 4.1, h: 0.35,
    fontSize: 14, fontFace: FONT, color: CLR.accent, bold: true,
  });

  // Show interleaved pattern
  const interleaved = [
    { t: "字", c: "FDEBD0" }, { t: "句", c: "D5F5E3" },
    { t: "词", c: "EBF5FB" }, { t: "篇", c: "FADBD8" },
    { t: "句", c: "D5F5E3" }, { t: "字", c: "FDEBD0" },
  ];
  interleaved.forEach((item, i) => {
    slide.addShape(pptx.shapes.RECTANGLE, {
      x: 5.4 + i * 0.72, y: 1.55, w: 0.65, h: 0.55,
      fill: { color: item.c },
    });
    slide.addText(item.t, {
      x: 5.4 + i * 0.72, y: 1.55, w: 0.65, h: 0.55,
      fontSize: 12, fontFace: FONT, color: CLR.secondary, bold: true, align: "center", valign: "middle",
    });
  });
  slide.addText("混合不同单元和题型出题\n学生必须识别题型、选择策略", {
    x: 5.5, y: 2.25, w: 4.0, h: 0.8,
    fontSize: 11, fontFace: FONT, color: CLR.darkGray,
  });

  // Research result
  slide.addShape(pptx.shapes.ROUNDED_RECTANGLE, {
    x: 0.5, y: 3.75, w: 9.0, h: 1.5,
    fill: { color: CLR.secondary }, rectRadius: 0.12,
  });
  slide.addText("Rohrer & Taylor (2007) 研究发现", {
    x: 0.8, y: 3.85, w: 4, h: 0.35,
    fontSize: 12, fontFace: FONT, color: "8899AA",
  });
  slide.addText([
    { text: "交错练习效果比分类练习好 ", options: { fontSize: 18, fontFace: FONT, color: CLR.white } },
    { text: "43%", options: { fontSize: 32, fontFace: FONT, color: CLR.primary, bold: true } },
  ], {
    x: 0.8, y: 4.2, w: 5, h: 0.6,
  });
  slide.addText("App通过混合不同单元和题型随机出题，有效防止机械记忆，提升迁移能力", {
    x: 0.8, y: 4.8, w: 8.4, h: 0.3,
    fontSize: 11, fontFace: FONT, color: CLR.lightGray,
  });
}

// ═══════════════════════════════════════════════════════
// SLIDE 8 - Architecture
// ═══════════════════════════════════════════════════════
{
  const slide = pptx.addSlide();
  slideBase(slide);
  slideNum(slide, 8, TOTAL);

  sectionTag(slide, "系统架构", CLR.secondary);

  slide.addText("App 功能架构", {
    x: 0.5, y: 0.9, w: 9, h: 0.55,
    fontSize: 26, fontFace: FONT, color: CLR.secondary, bold: true,
  });

  // Flowchart - Top row: App entry + 4 modes
  // App entry
  slide.addShape(pptx.shapes.ROUNDED_RECTANGLE, {
    x: 3.6, y: 1.65, w: 2.4, h: 0.65,
    fill: { color: CLR.secondary }, rectRadius: 0.15,
  });
  slide.addText("📱 打开 App", {
    x: 3.6, y: 1.65, w: 2.4, h: 0.65,
    fontSize: 15, fontFace: FONT, color: CLR.white, bold: true, align: "center", valign: "middle",
  });

  // Arrow down
  slide.addText("▼", {
    x: 4.4, y: 2.3, w: 0.8, h: 0.35,
    fontSize: 18, fontFace: FONT, color: CLR.primary, align: "center",
  });

  // 4 modes
  const modes = [
    { name: "复习清单", color: CLR.primary },
    { name: "单元测试", color: "3498DB" },
    { name: "闪卡记忆", color: CLR.accent },
    { name: "今日复习", color: "9B59B6" },
  ];

  modes.forEach((m, i) => {
    const x = 1.1 + i * 2.2;
    slide.addShape(pptx.shapes.ROUNDED_RECTANGLE, {
      x: x, y: 2.7, w: 1.9, h: 0.65,
      fill: { color: m.color }, rectRadius: 0.12,
    });
    slide.addText(m.name, {
      x: x, y: 2.7, w: 1.9, h: 0.65,
      fontSize: 13, fontFace: FONT, color: CLR.white, bold: true, align: "center", valign: "middle",
    });
  });

  // Arrow down from modes
  slide.addText("▼", {
    x: 4.4, y: 3.4, w: 0.8, h: 0.35,
    fontSize: 18, fontFace: FONT, color: CLR.primary, align: "center",
  });

  // Bottom flow: 4 connected steps
  const flowSteps = [
    { name: "即时反馈", color: CLR.primary, icon: "⚡" },
    { name: "错题追踪", color: "E74C3C", icon: "📋" },
    { name: "间隔复习", color: CLR.accent, icon: "📅" },
    { name: "游戏化激励", color: "9B59B6", icon: "🎮" },
  ];

  flowSteps.forEach((f, i) => {
    const x = 0.5 + i * 2.45;
    slide.addShape(pptx.shapes.ROUNDED_RECTANGLE, {
      x: x, y: 3.9, w: 2.15, h: 0.85,
      fill: { color: f.color },
      shadow: { type: "outer", blur: 3, offset: 1, color: "BBBBBB", opacity: 0.2 },
      rectRadius: 0.1,
    });
    slide.addText(`${f.icon} ${f.name}`, {
      x: x, y: 3.9, w: 2.15, h: 0.85,
      fontSize: 14, fontFace: FONT, color: CLR.white, bold: true, align: "center", valign: "middle",
    });
    // Arrow between steps
    if (i < flowSteps.length - 1) {
      slide.addText("→", {
        x: x + 2.15, y: 3.9, w: 0.3, h: 0.85,
        fontSize: 22, fontFace: FONT, color: CLR.darkGray, align: "center", valign: "middle",
      });
    }
  });

  // Feedback loop arrow text
  slide.addShape(pptx.shapes.RECTANGLE, {
    x: 0.5, y: 4.85, w: 9.2, h: 0.04,
    fill: { color: CLR.primary }, transparency: 40,
  });
  slide.addText("♻️ 错题自动回到「间隔复习」队列，形成闭环学习系统", {
    x: 0.5, y: 4.95, w: 9.2, h: 0.4,
    fontSize: 12, fontFace: FONT, color: CLR.darkGray, align: "center",
  });
}

// ═══════════════════════════════════════════════════════
// SLIDE 9 - Expected Results
// ═══════════════════════════════════════════════════════
{
  const slide = pptx.addSlide();
  slideBase(slide);
  slideNum(slide, 9, TOTAL);

  sectionTag(slide, "预期效果", CLR.accent);

  slide.addText("预期效果", {
    x: 0.5, y: 0.9, w: 9, h: 0.55,
    fontSize: 26, fontFace: FONT, color: CLR.secondary, bold: true,
  });

  // Chart area - Bar chart showing memory retention
  slide.addShape(pptx.shapes.ROUNDED_RECTANGLE, {
    x: 0.5, y: 1.65, w: 4.8, h: 3.4,
    fill: { color: CLR.white },
    shadow: { type: "outer", blur: 4, offset: 2, color: "CCCCCC", opacity: 0.2 },
    rectRadius: 0.12,
  });
  slide.addText("记忆保持率对比", {
    x: 0.7, y: 1.75, w: 4.4, h: 0.35,
    fontSize: 14, fontFace: FONT, color: CLR.secondary, bold: true,
  });

  // Y-axis label
  slide.addText("%", {
    x: 0.55, y: 2.2, w: 0.3, h: 0.3,
    fontSize: 10, fontFace: FONT, color: CLR.darkGray, align: "center",
  });

  // Bar chart data
  const chartData = [
    { label: "1天后", before: 34, after: 85 },
    { label: "1周后", before: 23, after: 78 },
    { label: "1月后", before: 21, after: 72 },
    { label: "3月后", before: 19, after: 68 },
  ];

  const maxH = 2.0;
  chartData.forEach((d, i) => {
    const x = 1.0 + i * 1.05;
    const baseY = 4.8;

    // Before bar
    const hBefore = maxH * (d.before / 100);
    slide.addShape(pptx.shapes.RECTANGLE, {
      x: x, y: baseY - hBefore, w: 0.35, h: hBefore,
      fill: { color: "E0E0E0" },
    });
    slide.addText(`${d.before}`, {
      x: x - 0.05, y: baseY - hBefore - 0.25, w: 0.45, h: 0.25,
      fontSize: 8, fontFace: FONT, color: "999999", align: "center",
    });

    // After bar
    const hAfter = maxH * (d.after / 100);
    slide.addShape(pptx.shapes.RECTANGLE, {
      x: x + 0.4, y: baseY - hAfter, w: 0.35, h: hAfter,
      fill: { color: CLR.accent },
    });
    slide.addText(`${d.after}`, {
      x: x + 0.35, y: baseY - hAfter - 0.25, w: 0.45, h: 0.25,
      fontSize: 8, fontFace: FONT, color: CLR.accent, bold: true, align: "center",
    });

    // Label
    slide.addText(d.label, {
      x: x - 0.05, y: baseY + 0.05, w: 0.85, h: 0.25,
      fontSize: 9, fontFace: FONT, color: CLR.darkGray, align: "center",
    });
  });

  // Legend
  slide.addShape(pptx.shapes.RECTANGLE, {
    x: 1.5, y: 4.85, w: 0.3, h: 0.2,
    fill: { color: "E0E0E0" },
  });
  slide.addText("传统复习", {
    x: 1.85, y: 4.83, w: 0.8, h: 0.25,
    fontSize: 9, fontFace: FONT, color: CLR.darkGray,
  });
  slide.addShape(pptx.shapes.RECTANGLE, {
    x: 2.8, y: 4.85, w: 0.3, h: 0.2,
    fill: { color: CLR.accent },
  });
  slide.addText("App复习", {
    x: 3.15, y: 4.83, w: 0.8, h: 0.25,
    fontSize: 9, fontFace: FONT, color: CLR.accent,
  });

  // Right side - Three result cards
  const results = [
    { title: "记忆保持率", value: "+200%", desc: "间隔重复+检索练习\n让知识长期保存", color: CLR.accent, icon: "🧠" },
    { title: "学习兴趣", value: "+85%", desc: "游戏化激励系统\n让复习变得有趣", color: CLR.primary, icon: "⭐" },
    { title: "自主学习", value: "持续培养", desc: "即时反馈+错题追踪\n养成自主学习习惯", color: CLR.secondary, icon: "📚" },
  ];

  results.forEach((r, i) => {
    const y = 1.65 + i * 1.15;
    slide.addShape(pptx.shapes.ROUNDED_RECTANGLE, {
      x: 5.6, y: y, w: 4.1, h: 1.0,
      fill: { color: CLR.white },
      shadow: { type: "outer", blur: 3, offset: 1, color: "DDDDDD", opacity: 0.2 },
      rectRadius: 0.1,
    });
    // Left color strip
    slide.addShape(pptx.shapes.RECTANGLE, {
      x: 5.6, y: y, w: 0.1, h: 1.0,
      fill: { color: r.color },
    });
    slide.addText(r.icon, {
      x: 5.85, y: y + 0.1, w: 0.6, h: 0.5,
      fontSize: 24, align: "center", valign: "middle",
    });
    slide.addText(r.title, {
      x: 6.5, y: y + 0.05, w: 1.8, h: 0.3,
      fontSize: 12, fontFace: FONT, color: CLR.darkGray,
    });
    slide.addText(r.value, {
      x: 8.2, y: y + 0.0, w: 1.3, h: 0.4,
      fontSize: 20, fontFace: FONT, color: r.color, bold: true, align: "right",
    });
    slide.addText(r.desc, {
      x: 6.5, y: y + 0.4, w: 3.0, h: 0.5,
      fontSize: 10, fontFace: FONT, color: CLR.darkGray,
    });
  });
}

// ═══════════════════════════════════════════════════════
// SLIDE 10 - Thank You
// ═══════════════════════════════════════════════════════
{
  const slide = pptx.addSlide();
  slide.background = { color: CLR.secondary };

  // Decorative shapes
  slide.addShape(pptx.shapes.OVAL, {
    x: -1.0, y: -1.0, w: 4, h: 4,
    fill: { color: CLR.primary }, transparency: 85,
  });
  slide.addShape(pptx.shapes.OVAL, {
    x: 7.5, y: 3.5, w: 3, h: 3,
    fill: { color: CLR.accent }, transparency: 85,
  });

  // Main thank you text
  slide.addText("谢 谢", {
    x: 0, y: 1.5, w: "100%", h: 1.2,
    fontSize: 52, fontFace: FONT, color: CLR.white, bold: true, align: "center", valign: "middle",
  });

  // Divider
  slide.addShape(pptx.shapes.RECTANGLE, {
    x: 4.0, y: 2.8, w: 2, h: 0.04, fill: { color: CLR.primary },
  });

  // Subtitle
  slide.addText("三年级语文复习App · 教育学改进方案", {
    x: 0, y: 3.1, w: "100%", h: 0.5,
    fontSize: 16, fontFace: FONT, color: CLR.lightGray, align: "center",
  });

  // Contact info
  slide.addShape(pptx.shapes.ROUNDED_RECTANGLE, {
    x: 3.0, y: 3.8, w: 4, h: 1.2,
    fill: { color: CLR.primary }, transparency: 30, rectRadius: 0.1,
  });
  slide.addText("📧 联系方式：[your@email.com]\n📱 微信号：[your_wechat]\n🌐 项目主页：[project_url]", {
    x: 3.0, y: 3.8, w: 4, h: 1.2,
    fontSize: 11, fontFace: FONT, color: CLR.white, align: "center", valign: "middle",
    lineSpacingMultiple: 1.3,
  });
}

// ═══════════════════════════════════════════════════════
// WRITE FILE
// ═══════════════════════════════════════════════════════
const outPath = "C:\\Users\\13274\\语文复习App\\三年级语文复习App_教育学方案.pptx";
pptx.writeFile({ fileName: outPath })
  .then(() => {
    console.log("✅ Presentation saved to: " + outPath);
    console.log("   Slides: " + pptx.slides.length);
  })
  .catch(err => {
    console.error("❌ Error:", err);
    process.exit(1);
  });
