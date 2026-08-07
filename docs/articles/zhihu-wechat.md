# 我把磁性 Skyrmion 家族做成了一个可交互的纹理图鉴

前段时间整理 magnetic skyrmion 的综述时，我一直觉得 Göbel、Mertig 和 Tretiakov 那篇 *Physics Reports* 里的 Fig. 2 很适合当作一张“磁性拓扑纹理地图”。Néel、Bloch、antiskyrmion、bimeron、biskyrmion、skyrmionium，甚至反铁磁和亚铁磁 skyrmion，都能在同一套图里找到位置。

静态图片也有一个明显限制：看懂某一张并不难，把不同纹理之间的关系真正连起来就麻烦很多。尤其是 polarity、vorticity、helicity 这三个参数，公式写下来很短，面对一圈圈颜色和箭头时，直觉往往还是断的。

所以我把这套东西做成了一个可以直接在浏览器里玩的交互网页：**磁性 Skyrmion 家族 · 交互纹理图鉴**。

【配图 1：网站整页截图。建议使用 Néel skyrmion 默认页面，能同时看到主图、Arrow field、Color field 和右侧解释。】

## 从三个参数重新看 skyrmion

对一个完整、近似轴对称的二维 skyrmion，可以把磁化场写成

$$
\mathbf m(\mathbf r)=
\begin{pmatrix}
\sin\theta\cos\Phi\\
\sin\theta\sin\Phi\\
\cos\theta
\end{pmatrix}.
$$

这里 $\theta$ 决定磁矩有多少分量朝向面外，$\Phi$ 决定面内磁矩指向哪里。对于理想轴对称纹理，最方便的一种写法是

$$
\Phi(\phi)=m\phi+\gamma.
$$

于是三个最常见的参数就有了非常直接的几何意义。

**polarity $p$** 看中心与远处背景的面外方向；**vorticity $m$** 看绕纹理中心一周时，面内磁化究竟旋转了几圈；**helicity $\gamma$** 则描述所有面内箭头相对径向统一偏转了多少。

对于这类完整 skyrmion，综述中给出

$$
N_{\mathrm{Sk}}=mp.
$$

这也解释了一个很容易混淆的地方：Néel、Bloch 和 intermediate-helicity skyrmion 可以拥有相同的拓扑荷。它们看起来差异很大，变化主要来自 helicity。

网页里我把 $p$、$m$、$\gamma$ 直接做成了滑块。拖动 helicity 时，可以连续看到一张径向的 Néel 纹理逐渐旋成 Bloch，再继续进入另一种中间状态。对我来说，这比盯着几张分开的示意图更容易建立直觉。

【配图 2：Néel outward、intermediate helicity、Bloch 三张主图并排。用于说明 γ 连续改变时，拓扑荷可以保持不变。】

## 13 个预设放进同一张地图

目前网页里放了 13 个预设：两种 Néel、两种 Bloch、intermediate-helicity、higher-order skyrmion、antiskyrmion、skyrmionium、biskyrmion、meron、bimeron，以及 antiferromagnetic 和 ferrimagnetic skyrmion。

我没有把它们简单做成 13 张可以切换的图片。主图旁边另外拆出了 **Arrow field** 和 **Color field**：前者只留下局域磁化箭头，后者只留下颜色编码。看 antiskyrmion、bimeron、biskyrmion 这类结构时，这种拆分尤其有用，因为复杂纹理里最容易混在一起的恰好就是“箭头怎么转”和“面外分量在哪里翻转”。

颜色规则保持统一：白色对应 $+z$，黑色对应 $-z$，彩色区域编码面内方向。于是从普通 skyrmion 切到 meron、skyrmionium 或 higher-order skyrmion 时，可以沿用同一套读图习惯。

## 有些纹理不能硬套 p、m、γ

做到 bimeron 和 biskyrmion 时，我发现一个很重要的边界：$p,m,\gamma$ 这套参数最适合描述完整、近似轴对称的二维 ferromagnetic skyrmion。到了复合纹理，继续把三个滑块全部开放会产生误导。

所以网页对 bimeron、biskyrmion、skyrmionium，以及反铁磁、亚铁磁 skyrmion，直接锁定了不适用的全局参数。右侧信息栏改用子纹理、核心关系、Néel order 或补偿关系来描述。

这个处理看起来只是一个 UI 细节，其实是我做这个小工具时最在意的地方之一。交互自由度越多，越容易让一个“可以拖的参数”在视觉上获得并不存在的物理意义。

## 反铁磁与亚铁磁 skyrmion

反铁磁和亚铁磁 skyrmion 也专门做了双子晶格分解。

理想的 antiferromagnetic skyrmion 可以看成 A、B 两个逐点反平行、磁矩幅值相等的子晶格纹理。净磁化发生局域补偿，更自然的描述量是 Néel order：

$$
\mathbf n(\mathbf r)=
\frac{\mathbf m_A(\mathbf r)-\mathbf m_B(\mathbf r)}{2}.
$$

网页里把 A/B 两套纹理上下拉开，仅用于教学观察。两个盘面的色标保持一致，真实的反平行关系由箭头方向表达。这个“层间距”没有材料结构含义。

Ferrimagnetic skyrmion 同样具有两个反平行子晶格，但两边磁矩大小不同，因此会留下非零净磁化。当前网页用不同的箭头长度表达这一点，同时把残余 $\mathbf M_{\mathrm{net}}$ 单独标出来。箭头长度比例属于教学可视化参数，并不对应某一种特定材料的固定数值。

【配图 3：AFM 与 FiM 主图并排。图注注明“上下分层仅为教学拆解”。】

## 我最想保留的是原文定位

这个网页的目标仍然是辅助读论文，所以每个预设右侧都保留了对应的原文定位：Fig.、Section 和页码。需要进一步确认定义、实验体系或材料背景时，可以直接回到 Göbel 等人的综述。

原论文是：

Börge Göbel, Ingrid Mertig, Oleg A. Tretiakov, *Beyond skyrmions: Review and perspectives of alternative magnetic quasiparticles*, **Physics Reports 895, 1–28 (2021)**。

DOI：10.1016/j.physrep.2020.10.001

这篇综述本身是 Open Access、CC BY。网页里也保留了 DOI 和原文 PDF 入口，方便把交互图和原图来回对照。

我此前还整理过一篇更完整的中文综述笔记：

[磁性 Skyrmion 家族综述：从 Néel、Bloch 到 Meron、Hopfion](https://zhuanlan.zhihu.com/p/2069027257536999823)

网页更偏几何直觉和交互，长文更偏完整知识脉络，两者可以配着看。

## 做成网页之后，一些关系突然变得很直观

我自己最明显的感受有几个。

第一，Néel 与 Bloch 的差异真的应该从 helicity 看。只比较两张静态图，很容易把它们当作两个孤立类别；连续拖动 $\gamma$ 以后，它们在几何上的联系非常自然。

第二，meron、bimeron 和 skyrmion 的关系也更清楚。meron 只完成从面外到面内的半程翻转，bimeron 则可以理解为面内背景中的双核心组合。把颜色场单独拿出来后，外围背景究竟是面内还是面外，一眼就能看到。

第三，skyrmionium 与 biskyrmion 虽然都属于“组合纹理”，几何逻辑差别很大。一个沿径向形成内外反向绕转，一个由两个同号核心部分重叠。把子核心位置、Arrow field 和 Color field 同时对应起来，读 Fig. 2 和 Fig. 8 会轻松很多。

第四，反铁磁和亚铁磁 skyrmion 很适合显式画出两个子晶格。只画一张普通 skyrmion 色盘，会把补偿关系完全藏起来。拆开以后，$M\approx0$ 与 $M\neq0$ 的区别才真正落到图像上。

## 开源与在线使用

整个工具目前是一个单文件静态网页，没有前端框架依赖，下载后直接打开 `index.html` 就可以离线运行。我也把完整知识笔记、原始综述 PDF 和科学交互网页的迭代审计方法一起整理进了仓库。

GitHub：[https://github.com/Xin-Jiaqi/skyrmion-texture-atlas](https://github.com/Xin-Jiaqi/skyrmion-texture-atlas)

在线体验：[https://xin-jiaqi.github.io/skyrmion-texture-atlas/](https://xin-jiaqi.github.io/skyrmion-texture-atlas/)

网页支持直接导出当前主磁纹理 PNG。如果只是想在笔记、组会或课堂里快速找一张结构示意，也可以把它当作一个小型图形生成器使用。

目前这版主要覆盖二维纹理。原综述后面还有 skyrmion tube、chiral bobber 和 hopfion 等三维对象，这部分暂时留给以后继续扩展。

如果你正在学 skyrmion，希望这个小工具能帮你少在几张静态箭头图之间来回切换几次。
