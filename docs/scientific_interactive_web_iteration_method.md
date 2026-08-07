# 科学交互网页的迭代与审计方法

## 核心原则

不要把“代码能运行”当成“可以交付”。

一个科学可视化网页至少需要同时通过：

1. 科学性
2. 视觉质量
3. 排版与响应式布局
4. 交互状态
5. 浏览器实际渲染
6. PDF / 导出结果

并且：

> 每次正式交付前，至少内部迭代 3 版。
> 每一版都必须先看实际输出，再决定是否继续返工。
> 截图的目的不是证明“我检查过”，而是用来发现问题。

---

## 0. 先复述用户需求，建立验收清单

开始修改前，把用户要求逐条重新写成可检查的条件。

例如：

- [ ] 新增哪些科学对象？
- [ ] 哪些参数允许调节？
- [ ] 哪些参数必须锁定？
- [ ] 主图究竟显示真实磁化、序参量还是某个子晶格？
- [ ] 页面是否必须单屏完成？
- [ ] 右栏和底部是否需要严格对齐？
- [ ] 是否需要 PDF / DOI / 延伸阅读？
- [ ] 面向什么语言和地区？
- [ ] 哪些分辨率必须支持？

这样可以防止“做了很多，但漏了用户真正要求的东西”。

---

# 第一轮：科学结构正确

## 1. 先处理物理模型，再处理 UI

对于每个预设先回答：

1. 它是什么物理对象？
2. 是单一纹理还是复合纹理？
3. 哪些参数具有全局意义？
4. 哪些参数不能强行套用？
5. 主图应该画什么物理量？
6. 原文对应哪一节、哪一幅图？

例如：

### 普通 skyrmion

可以使用：

- polarity p
- vorticity m
- helicity γ
- topological charge N

因此基础参数可以开放。

### Biskyrmion / Bimeron

是复合纹理。

不能简单把整个对象视为一个具有唯一：

- p
- m
- γ

的轴对称 skyrmion。

因此：

- 锁定不适用的滑块；
- 使用 Composite view；
- 改用子纹理关系描述。

### Antiferromagnetic skyrmion

不能把净磁化 M(r) 画成普通 ferromagnetic skyrmion。

更合适的是：

n(r) = [m_A(r) - m_B(r)] / 2

即 Néel order parameter。

需要明确：

m_B(r) = -m_A(r)

M(r) ≈ 0

而 Néel order 仍可具有非平庸拓扑。

### Ferrimagnetic skyrmion

两个子晶格：

m_B(r) ≈ -η m_A(r),  0 < η < 1

因此：

M(r) ≠ 0

网页应显示：

- 主导子晶格方向；
- 另一子晶格反平行但磁矩幅值较小；
- 不能误画成单一 ferromagnetic skyrmion。

---

# 第二轮：视觉与信息架构

## 2. 浏览器截图，而不是只看 HTML/CSS

至少检查：

- 默认预设
- 最复杂复合预设
- 新增预设
- 参数锁定状态
- 高级参数展开状态

推荐尺寸：

- 1632 × 1088
- 1440 × 900
- 1366 × 768

每张截图人工检查：

### 科学

- 箭头方向是否正确？
- 颜色含义是否正确？
- 核心数量是否正确？
- 子纹理是否能够一一对应？
- 标签有没有误导？

### 美观

- 主图是否是视觉中心？
- 箭头粗细是否协调？
- 字号层级是否统一？
- 留白是否合理？
- 中英文是否混乱？
- 是否仍然有“后台页面 / 草稿页”的感觉？

### 排版

- 有没有遮挡？
- 有没有裁切？
- 是否出现大块无意义空白？
- 左右底部是否对齐？
- 右栏长文本如何滚动？
- 资源卡是否始终可访问？

如果截图中肉眼能发现问题：
不要交付，继续下一版。

---

# 第三轮：DOM / 几何程序化审计

## 3. 不依赖肉眼检查所有预设

为每一个 preset 自动读取：

```js
document.documentElement.scrollWidth
document.documentElement.clientWidth
document.documentElement.scrollHeight
document.documentElement.clientHeight
```

检查：

```text
scrollWidth <= clientWidth
scrollHeight <= clientHeight
```

避免页面级 overflow。

---

## 4. 检查组件相交面积

读取：

```js
element.getBoundingClientRect()
```

对：

- sliders
- view controls
- advanced settings
- resource card
- right rail

计算矩形 overlap area。

必须满足：

```text
overlap = 0
```

特别注意：

> 默认折叠状态没有重叠，
> 并不代表高级参数展开后没有重叠。

所以必须分别测试交互状态。

---

## 5. 检查严格对齐

例如要求：

右栏底边 = 左下控制区底边

实际检查：

```text
abs(infoCard.bottom - controlsCard.bottom) < tolerance
```

理想情况下：

```text
bottom delta = 0 px
```

不要仅凭截图“看起来差不多”。

---

# 第四轮：交互状态测试

## 6. 自动执行真实用户操作

至少包括：

### Preset 切换

逐个切换全部预设。

确认：

- 无 JavaScript error
- 标题正确
- 参数正确
- 图例正确
- source focus 正确

### 参数锁定

例如复合纹理：

```js
p.disabled === true
m.disabled === true
gamma.disabled === true
```

普通 skyrmion：

```js
disabled === false
```

### Reset / 恢复预设

先故意修改：

- p
- m
- γ
- c
- β
- q
- rings
- L

再点击“恢复预设”。

检查全部恢复，而不是只恢复 p/m/γ。

### Advanced settings

展开高级参数。

检查：

- 面板仍在 viewport 内；
- 不覆盖视角按钮；
- 不产生页面滚动；
- 可以重新关闭。

### Modal

打开术语解释。

检查：

- 不超出 viewport；
- 字体和公式正常；
- 可以关闭。

---

# 第五轮：全预设测试

## 7. 不只测试自己刚修改的预设

新功能可能破坏旧功能。

因此每次最终版本必须重新测试所有 preset。

对每个 preset 记录：

- JS errors
- page overflow
- internal scroll
- parameter lock states
- legend
- title
- source
- bottom alignment
- overlap area

原则：

> 新增一个功能，也要回归测试整个网站。

---

# 第六轮：PDF / 导出审计

## 8. 浏览器截图通过 ≠ PDF 一定通过

实际执行：

```text
HTML
↓
浏览器 PDF export
↓
PDF
↓
独立 PDF renderer
↓
PNG
```

然后重新人工检查。

重点：

- 字体有没有变化？
- 中文有没有掉字？
- 公式有没有错位？
- 卡片有没有裁切？
- Canvas 有没有变黑？
- 控件有没有跑位？

---

## 9. 最好使用两个 PDF renderer

例如：

- pdfium
- pdftoppm

比较两个 renderer 输出。

若只有约 0.x% 像素差异，并且差异集中于：

- 字体 hinting
- anti-aliasing
- subpixel rendering

通常可以接受。

如果出现：

- 卡片位移
- 文字丢失
- 图片裁切
- 黑块
- glyph 缺失

必须返工。

---

# 第七轮：科学审计

## 10. 对照论文，而不是凭记忆写

每个预设至少记录：

- 原文 Figure
- 原文 Section
- 页码
- 定义
- 是否实验观测
- 是否理论预测
- 程序中的表示方式是否为原文直接图像，还是教学模型

尤其注意区分：

### 原文事实

“论文明确写了什么。”

### 教学表示

“网页为了帮助理解采用什么简化。”

不能把教学模型伪装成论文原始定义。

---

# 第八轮：面向正式发布

## 11. 删除开发者口吻

不要出现：

- “当前会话 PDF”
- “本地工作副本”
- “这个按钮只是……”
- “为了测试……”
- “customized”
- 开发过程说明

成品只保留读者真正需要的信息。

---

## 12. 中文科学网站建议

面向中文用户时：

### 中文优先

例如：

- 纹理摘要 · Texture brief
- 箭头场 · Arrow field
- 颜色场 · Color field

### 但保留核心英文术语

例如：

- skyrmion
- helicity
- vorticity
- Néel
- Bloch
- topological charge

方便科研检索。

### 不依赖不稳定外部服务

核心可视化尽量：

- 不依赖 CDN
- 不依赖 Google Fonts
- 不依赖外部 JS framework

让网页本地打开仍然完整可用。

---

# 最终交付条件

只有同时满足下面条件才交付：

- [ ] 用户需求逐项完成
- [ ] 至少 3 次内部迭代
- [ ] 浏览器截图人工检查
- [ ] DOM 几何检查
- [ ] 全预设测试
- [ ] 交互状态测试
- [ ] 参数物理边界检查
- [ ] PDF 导出
- [ ] PDF → PNG 独立渲染
- [ ] 至少一种 PDF renderer 验证
- [ ] 复杂任务最好进行双 renderer parity
- [ ] 没有遮挡
- [ ] 没有裁切
- [ ] 没有页面 overflow
- [ ] 没有 JS error
- [ ] 科学表述有论文依据
- [ ] 教学简化明确标注
- [ ] 文案达到正式发布状态

最重要的一条经验：

> “检查”不是一个动作，而是一个反馈循环：
>
> 实现 → 导出 → 观察 → 找问题 → 返工 → 再导出。
>
> 如果截图已经暴露出问题，那么这次检查尚未完成。
