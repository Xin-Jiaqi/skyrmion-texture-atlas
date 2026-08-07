# 磁性 Skyrmion 拓扑纹理图鉴 · 使用指南

本文档对应仓库根目录的 `index.html`。内容面向中文读者，保留英文科学术语作为检索关键词，并包含原文 PDF、知乎延伸阅读、反铁磁与亚铁磁 skyrmion 预设。

## 本版资源

- **延伸阅读**：[磁性 Skyrmion 家族综述：从 Néel、Bloch 到 Meron、Hopfion - 辛嘉琪](https://zhuanlan.zhihu.com/p/2069027257536999823)
- **原文**：Börge Göbel, Ingrid Mertig, Oleg A. Tretiakov, *Physics Reports* **895** (2021) 1–28, DOI: 10.1016/j.physrep.2020.10.001
- 原文为 open-access **CC BY**；网页打包版同时包含本地 PDF，便于直接下载与离线阅读。

---

# 磁性 Skyrmion 拓扑纹理图鉴 — 帮助与完整知识笔记

## A. 程序使用说明

这个网页把主要信息压缩在一个桌面视口内：

- **左侧主图**：底色 + 箭头的完整磁化纹理。
- **右上箭头场**：只看局域磁化箭头。
- **右下颜色场**：只看颜色编码。
- **最右信息栏**：随预设切换，显示几何定义、识别要点、拓扑信息与原文位置。
- **底部控制区**：polarity、vorticity、helicity、视角切换；高级参数默认折叠。

### 交互

- 左键拖动：旋转
- 滚轮：缩放
- Shift + 左键 / 右键拖动：平移
- 论文视角 / 俯视 / 侧视 / 恢复预设：快速切换

### 当前高级默认值

- 中心白区 `c = 0.11`
- 灰黑外圈 `β = 0.995`
- 外圈收束 `q = 3`
- 箭头环数 `10`
- 箭头长度 `L = 0.20`

### 当前程序预设

1. Néel skyrmion · outward
2. Néel skyrmion · inward
3. Bloch skyrmion · CW
4. Bloch skyrmion · CCW
5. Intermediate-helicity skyrmion
6. Higher-order skyrmion · m=2
7. Antiskyrmion
8. Skyrmionium
9. Biskyrmion
10. Meron
11. Bimeron
12. 反铁磁 skyrmion · Antiferromagnetic skyrmion
13. 亚铁磁 skyrmion · Ferrimagnetic skyrmion

> **参数边界**：单一 `p,m,γ` 最适合完整、近似轴对称的二维 ferromagnetic skyrmion。Bimeron、biskyrmion、skyrmionium，以及反铁磁 / 亚铁磁 skyrmion 会在网页中锁定不适用的基础参数，并改用复合构型、子晶格关系、Néel order 或补偿关系描述。
>
> **反铁磁表示**：主图显示 Néel order `n(r)`，不是净磁化 `M(r)`；A/B 子晶格磁矩逐点反平行并局域补偿。
>
> **亚铁磁表示**：主图采用 A/B 双子晶格分解视图。两套纹理逐点反平行，颜色使用同一方向色标；磁矩幅值差异只通过箭头长度表示。当前取 $|m_B|\approx0.70|m_A|$ 作为教学示意，因此保留非零净磁化。

---

## B. 完整文献知识笔记

下面保留并整合原 Markdown 笔记的全部内容，作为程序的知识底座。

# 可调用文献笔记

## 文献信息

- **题目**：Beyond skyrmions: Review and perspectives of alternative magnetic quasiparticles
- **作者**：Börge Göbel, Ingrid Mertig, Oleg A. Tretiakov
- **期刊**：Physics Reports 895, 1–28 (2021)
- **DOI**：10.1016/j.physrep.2020.10.001
- **文章类型**：综述
- **核心主题**：以传统磁性 skyrmion 为参照，分类并比较 antiskyrmion、meron、bimeron、biskyrmion、skyrmionium、反铁磁/亚铁磁 skyrmion，以及 skyrmion tube、chiral bobber、hopfion 等拓扑磁纹理。
- **最重要图像入口**：Fig. 1 给出总分类；Fig. 2(a–l) 集中展示主要纹理；Fig. 3 给出 skyrmion 的几何构造；Fig. 8 对比若干复合纹理的拓扑荷密度与面外磁化。

## 核心理解

这篇综述可以当作一张“拓扑磁纹理地图”。全文的组织逻辑可以压缩为三条构造路径：

1. **改变单个基本纹理内部的绕转方式**：得到 Néel、Bloch、intermediate-helicity skyrmion、antiskyrmion 和 higher-order skyrmion。
2. **组合多个基本纹理，或改变承载纹理的磁性背景**：得到 bimeron、biskyrmion、skyrmionium、反铁磁和亚铁磁 skyrmion。
3. **把二维纹理向第三维延伸、截断或闭合**：得到 skyrmion tube、chiral bobber 和 hopfion。

理解这些对象时，最有效的顺序是：

$$
\text{磁化场的几何绕转}
\longrightarrow
\text{拓扑荷与分类参数}
\longrightarrow
\text{多个子纹理如何组合}
\longrightarrow
\text{二维纹理如何进入三维}
$$

本文对传统 skyrmion 的介绍集中在 Sec. 2，覆盖拓扑、几何、稳定机制和涌现电动力学。Sec. 3 将这些概念作为参照，系统讨论替代磁准粒子。对于初学者，Fig. 2、Fig. 3、Eqs. (1)–(7) 和 Fig. 8 构成最重要的入门路径。

---

## 一、读图方法与几何语言

### 1. Fig. 2 中颜色和箭头的含义

- **箭头方向**：局域归一化磁化 $\mathbf m(\mathbf r)$ 的方向。
- **白色区域**：正的面外分量，通常对应 $m_z>0$。
- **黑色区域**：负的面外分量，通常对应 $m_z<0$。
- **彩色区域**：不同的面内磁化方位角。颜色绕中心循环一次，通常表示面内方向完成一次 $2\pi$ 绕转。

观察任意纹理时，可以依次回答五个问题：

1. 中心磁矩朝 $+z$、$-z$，还是位于面内？
2. 远处背景朝哪个方向？
3. 从中心向外，磁矩翻转了几次？
4. 在实空间绕中心一周，面内磁矩旋转了几圈？
5. 面内磁矩相对径向是平行、垂直，还是介于两者之间？

前三个问题主要决定 polarity 和径向结构；第四个问题决定 vorticity；第五个问题决定 helicity 或纹理取向。

### 2. 自旋球面覆盖的直观图像

二维磁化场把每一个实空间位置 $\mathbf r=(x,y)$ 映射到单位球面上的一个磁化方向 $\mathbf m(\mathbf r)$。

- 完整 skyrmion 通常覆盖整个自旋球面一次，因此具有整数拓扑荷。
- meron 只覆盖半个自旋球面，因此常具有半整数拓扑荷。
- higher-order skyrmion 对球面进行多次覆盖，因此 $|N_{\mathrm{Sk}}|>1$。
- skyrmionium 的不同径向区域覆盖方向相反，总拓扑荷相互抵消。

Fig. 3(a–c) 给出最直观的构造：三维 hedgehog 的球面被展开成二维圆盘，磁化方向仍然覆盖整个单位球面；沿第三维直接延伸后得到 skyrmion tube。

---

## 二、Polarity、vorticity、helicity 与拓扑荷

### 1. 磁化场的角度表示

二维归一化磁化场写为

$$
\mathbf m(\mathbf r)=
\begin{pmatrix}
\sin\theta\cos\Phi\\
\sin\theta\sin\Phi\\
\cos\theta
\end{pmatrix},
$$

其中：

- $\theta$：磁矩相对 $+z$ 的极角，决定面外分量；
- $\Phi$：磁矩在 $xy$ 平面内的方位角；
- 实空间位置写作 $\mathbf r=r(\cos\phi,\sin\phi)$，$\phi$ 是位置方位角。

对于理想轴对称 skyrmion，通常有

$$
\theta=\theta(r),\qquad \Phi=\Phi(\phi).
$$

### 2. 拓扑荷密度与总拓扑荷

论文 Eqs. (1)–(2)：

$$
N_{\mathrm{Sk}}
=
\int n_{\mathrm{Sk}}(\mathbf r)\,d^2r,
$$

$$
n_{\mathrm{Sk}}(\mathbf r)
=
\frac{1}{4\pi}
\mathbf m(\mathbf r)\cdot
\left[
\frac{\partial\mathbf m}{\partial x}
\times
\frac{\partial\mathbf m}{\partial y}
\right].
$$

几何上，$N_{\mathrm{Sk}}$ 记录磁化方向覆盖自旋单位球面的次数和方向。局域密度 $n_{\mathrm{Sk}}(\mathbf r)$ 则告诉我们拓扑绕转主要集中在哪些空间区域。

### 3. Polarity：中心与背景的面外反转

论文 Eq. (4)：

$$
p
=
-\frac12
\left[
\cos\theta(\infty)-\cos\theta(0)
\right]
=
\frac{\cos\theta(0)-\cos\theta(\infty)}{2}.
$$

对于完整 skyrmion：

- 中心朝 $+z$、背景朝 $-z$：$p=+1$；
- 中心朝 $-z$、背景朝 $+z$：$p=-1$。

最短理解：

> polarity 只比较中心和远处背景的面外方向。

### 4. Vorticity：绕中心一周时面内自旋转几圈

论文 Eq. (5)：

$$
m
=
\frac{\Phi(2\pi)-\Phi(0)}{2\pi},
$$

其中

$$
m=0,\pm1,\pm2,\ldots
$$

含义：沿实空间方位角 $\phi$ 绕纹理中心一周，面内磁化方位角 $\Phi$ 改变了多少个 $2\pi$。

- $m=+1$：沿一个方向转一圈；
- $m=-1$：沿相反方向转一圈；
- $|m|>1$：发生多重绕转。

最短理解：

> vorticity 描述面内磁化绕中心旋转的圈数和方向。

### 5. Helicity：面内磁化相对径向偏转多少

论文 Eq. (7)：

$$
\Phi(\phi)=m\phi+\gamma.
$$

对于 $m=+1$ 的圆对称 skyrmion，$\gamma$ 表示面内磁化相对实空间径向的统一偏移：

| $\gamma$ | 类型 | 面内磁化外观 |
|---:|---|---|
| $0$ | Néel | 径向朝外 |
| $\pi$ | Néel | 径向朝内 |
| $+\pi/2$ | Bloch | 沿一种圆周切向旋转 |
| $-\pi/2$ | Bloch | 沿相反圆周切向旋转 |
| 其他角度 | intermediate | 介于径向与切向之间 |

最短理解：

> helicity 决定面内箭头相对径向方向“歪了多少”。

### 6. 三个参数与拓扑荷的关系

对于完整、轴对称的二维 skyrmion，论文 Eq. (6) 给出

$$
\boxed{N_{\mathrm{Sk}}=mp}.
$$

由此得到：

- 改变 $p$：拓扑荷变号；
- 改变 $m$：拓扑荷的符号或绝对值改变；
- 改变 $\gamma$：拓扑荷不变，纹理外观和动力学可以显著改变。

因此，Néel、Bloch 和 intermediate skyrmion 可以拥有相同的 $N_{\mathrm{Sk}}$。它们的差别主要体现在 helicity。antiskyrmion 具有相反 vorticity，并表现出不同的空间对称性。

对于理想 meron，可以把半球覆盖写成

$$
N_{\mathrm{meron}}\approx\frac{mp}{2}=\pm\frac12.
$$

这条式子是对完整 skyrmion 公式的半球覆盖推广。论文正文主要通过 Fig. 4(c) 和 meron–antimeron lattice 说明其半整数拓扑荷。

### 7. 适用边界

单一的 $p,m,\gamma$ 最适合描述完整、近似轴对称的二维 skyrmion。以下对象需要扩展描述：

- antiskyrmion：$\gamma$ 更接近各向异性纹理相对晶轴的取向角；
- bimeron：使用背景磁化方向 $\alpha$ 和双核心连线方向 $\gamma$；
- biskyrmion、skyrmionium：需要分别描述多个子 skyrmion；
- 反铁磁/亚铁磁 skyrmion：需要分别描述两个子晶格；
- hopfion：使用三维 Hopf invariant $Q_H$。

---

## 三、分类框架：所有对象之间的关系

### 1. 基本二维拓扑单元

$$
\boxed{\text{skyrmion 与 meron}}
$$

- **skyrmion**：完整自旋球面覆盖，典型 $N_{\mathrm{Sk}}=\pm1$。
- **meron**：半球覆盖，典型 $N_{\mathrm{Sk}}=\pm1/2$。

### 2. 改变单个 skyrmion 的内部绕转

$$
\boxed{
\text{Néel}
\quad
\text{Bloch}
\quad
\text{intermediate}
\quad
\text{antiskyrmion}
\quad
\text{higher-order}
}
$$

- Néel、Bloch、intermediate：主要改变 helicity；
- antiskyrmion：改变 vorticity，并引入明显各向异性；
- higher-order：增加绕转次数，$|m|>1$。

### 3. 组合多个基本纹理

$$
\boxed{
\text{bimeron}
\quad
\text{biskyrmion}
\quad
\text{skyrmionium}
}
$$

- bimeron：meron 与 antimeron 的组合；
- biskyrmion：两个部分重叠、同号拓扑荷的 skyrmion；
- skyrmionium：内外拓扑荷相反的同心结构。

### 4. 改变磁性背景

$$
\boxed{
\text{antiferromagnetic skyrmion}
\quad
\text{ferrimagnetic skyrmion}
}
$$

- 反铁磁 skyrmion：两个等强度、方向相反的子晶格 skyrmion；
- 亚铁磁 skyrmion：两个方向相反但磁矩大小不同的子晶格 skyrmion。

### 5. 向三维扩展

$$
\boxed{
\text{skyrmion tube}
\quad
\text{chiral bobber}
\quad
\text{hopfion}
}
$$

- tube：二维 skyrmion 沿第三维延伸；
- bobber：tube 在 Bloch point 处终止；
- hopfion：tube 弯曲并闭合成环。

### 6. 一张关系树

```text
基本二维拓扑单元
├── skyrmion
│   ├── 按 helicity：Néel / Bloch / intermediate
│   ├── 按 vorticity：skyrmion / antiskyrmion / higher-order
│   ├── 组合
│   │   ├── biskyrmion：两个同号 skyrmion 部分重叠
│   │   └── skyrmionium：内外反号 skyrmion 同心嵌套
│   ├── 改变磁性背景
│   │   ├── antiferromagnetic skyrmion
│   │   └── ferrimagnetic skyrmion
│   └── 三维延伸
│       ├── skyrmion tube
│       ├── chiral bobber
│       └── hopfion
└── meron
    ├── meron / antimeron
    └── bimeron：meron + antimeron
```

Fig. 1 对应这棵关系树的更一般版本：基本激发、变体和二维/三维扩展。

---

## 四、基本 skyrmion 及 helicity 分类

### 1. 一般 magnetic skyrmion

#### 外观

- 中心磁矩与远处背景方向相反；
- 中间磁矩连续经过面内方向；
- 磁化方向从中心到外围完整覆盖一次单位球面；
- 典型拓扑荷为 $N_{\mathrm{Sk}}=\pm1$。

#### 最重要位置

- **Fig. 3(a)**：二维 Néel skyrmion；
- **Fig. 3(b)**：三维 hedgehog/Bloch point；
- **Fig. 3(c)**：二维 skyrmion 延伸成 skyrmion tube；
- **Sec. 2.1，pp.3–5**：拓扑与几何表征。

#### 物理直观

可以将 Fig. 3(b) 的 hedgehog 球面剪开并压平。压平后得到二维圆盘，磁化方向仍覆盖整个球面。连续磁化场若要变成均匀铁磁态，需要改变这种整体覆盖结构。

### 2. Néel skyrmion

#### 外观

- 面内磁矩沿实空间径向；
- 可以统一朝外，也可以统一朝内；
- 俯视时具有放射状“刺猬”外观。

#### 参数

Fig. 3(a) 的具体例子：

$$
p=+1,\qquad m=+1,\qquad \gamma=0,
$$

$$
N_{\mathrm{Sk}}=+1.
$$

一般情况：

- 径向朝外：$\gamma=0$；
- 径向朝内：$\gamma=\pi$。

#### 最重要位置

- **Fig. 3(a)，p.4**；
- **p.5，Eq. (8) 后的文字**；
- **Eq. (13)，p.7**：界面型 DMI 通常稳定 Néel skyrmion。

### 3. Bloch skyrmion

#### 外观

- 面内磁矩垂直于径向；
- 箭头沿圆周切向排列；
- 俯视时具有旋转漩涡外观。

#### 参数

$$
m=+1,\qquad \gamma=\pm\frac{\pi}{2},
$$

$$
N_{\mathrm{Sk}}=p.
$$

两种 $\gamma$ 对应相反的切向旋转方向。

#### 最重要位置

- **Fig. 4(b)，p.6**：Bloch skyrmion lattice；
- 图注明确给出 $m=+1,\gamma=-\pi/2$；
- **p.5**：Bloch 型面内磁化垂直于位置矢量；
- **Eq. (15)，p.7**：体相 DMI 稳定 Bloch skyrmion。

### 4. Intermediate-helicity skyrmion

#### 外观

- 基本保持圆对称；
- 面内磁矩同时具有径向和切向分量；
- 可理解为将 Néel skyrmion 的全部面内箭头统一旋转角度 $\gamma$。

#### Fig. 2(b) 的参数

$$
p=+1,\qquad m=+1,\qquad \gamma=\frac{\pi}{4},
$$

$$
N_{\mathrm{Sk}}=+1.
$$

#### 最重要位置

- **Fig. 2(b)，p.4**；
- **Sec. 3.1.1，p.12**；
- **Fig. 7(a,b)，p.15**：特定 helicity 可以改变电流驱动方向。

### 5. 三者的核心区别

Néel、Bloch 和 intermediate skyrmion 可以具有相同的 $p$、$m$ 和 $N_{\mathrm{Sk}}$。三者主要通过 $\gamma$ 区分：

$$
\text{Néel}
\xleftrightarrow{\ \gamma\ }
\text{intermediate}
\xleftrightarrow{\ \gamma\ }
\text{Bloch}.
$$

因此，helicity 改变的是面内纹理的几何朝向。拓扑荷保持不变。

---

## 五、Antiskyrmion 与 higher-order skyrmion

### 1. Antiskyrmion

#### 几何定义

普通 skyrmion 常取

$$
m=+1,
$$

antiskyrmion 则具有

$$
m=-1.
$$

在实空间绕中心一周时，面内磁化沿相反方向旋转。

#### 外观

- 沿特定主轴具有 Néel-like 截面；
- 沿对角方向具有 Bloch-like 截面；
- 连续圆对称性消失；
- 常呈四瓣或交替变化的各向异性外观。

Fig. 2(a) 给出

$$
m=-1,\qquad N_{\mathrm{Sk}}=-1.
$$

由 $N_{\mathrm{Sk}}=mp$ 可知该图对应 $p=+1$。整体反转中心和背景后，$p$ 与 $N_{\mathrm{Sk}}$ 同时变号。

#### Helicity 的特殊含义

对圆对称 skyrmion，$\gamma$ 是所有面内磁矩相对径向的统一偏移。对 antiskyrmion，$\gamma$ 更接近整个各向异性纹理相对晶轴的旋转取向。

#### 最重要位置

- **Fig. 2(a)，p.4**：理想 antiskyrmion；
- **Sec. 3.1.2，p.13**：几何、DMI 和运动；
- **Fig. 6(a)，p.14**：实验 LTEM 图；
- **Fig. 7(e,f)，p.15**：特定取向下的直线运动。

### 2. Higher-order skyrmion

#### 定义

$$
|m|>1,
$$

因此

$$
|N_{\mathrm{Sk}}|=|mp|>1.
$$

#### 外观

- 面内磁化绕中心旋转多次；
- 颜色在 Fig. 2(c) 中出现多重循环；
- 仍可具有单一中心，但内部绕转次数高于普通 skyrmion。

#### 最重要位置

- **Fig. 2(c)，p.4**：$N_{\mathrm{Sk}}=2$ 的 higher-order skyrmion；
- **Sec. 3.1，p.12**：与不同 vorticity 的 skyrmion 一并讨论。

---

## 六、Meron、antimeron 与 bimeron

### 1. Meron

#### 几何关系

完整 skyrmion 的径向变化可以写成

$$
+z\longrightarrow \text{面内}\longrightarrow -z,
$$

meron 只完成

$$
\pm z\longrightarrow \text{面内}.
$$

因此 meron 覆盖半个自旋球面，典型拓扑荷为

$$
N_{\mathrm{meron}}=\pm\frac12.
$$

#### 外观

- 中心磁矩朝 $+z$ 或 $-z$；
- 从中心向外逐渐转入面内；
- 远处背景位于面内；
- 单个 meron 常依附于更大的非共线背景或与其他 meron 组合。

### 2. Meron 与 antimeron

主要差别是 vorticity：

$$
m_{\mathrm{meron}}=+1,\qquad
m_{\mathrm{antimeron}}=-1.
$$

Fig. 4(c) 的 meron–antimeron lattice 中：

- meron：$m=+1$、$N_{\mathrm{Sk}}=+1/2$；
- antimeron：$m=-1$、$N_{\mathrm{Sk}}=+1/2$。

两者拓扑荷同号，意味着核心 polarity 也相反。该例中可理解为

$$
\begin{aligned}
\text{meron}:&\quad m=+1,\ p=+1,\\
\text{antimeron}:&\quad m=-1,\ p=-1.
\end{aligned}
$$

### 3. Bimeron

#### 组成关系

$$
\boxed{\text{bimeron}=\text{meron}+\text{antimeron}}.
$$

两个子粒子具有：

- 相反 vorticity；
- 相反 polarity；
- 同号的半整数拓扑荷。

因此

$$
\frac12+\frac12=1
$$

或整体反转后得到 $-1$。

#### 第二种理解

将普通 skyrmion 的全部自旋在自旋空间中整体旋转 $90^\circ$，可以得到 bimeron。于是 bimeron 也可视为面内磁化背景中的 skyrmion。

#### 外观

- 远处背景磁矩位于面内；
- 内部有两个面外核心；
- 一个核心朝 $+z$，另一个朝 $-z$；
- 两个核心形成双瓣或偶极子式结构。

#### 参数与图中数值

- Fig. 2(d)：$N_{\mathrm{Sk}}=-1$；
- Fig. 8(a)：$N_{\mathrm{Sk}}=+1$。

bimeron 没有单一的全局 $p,m,\gamma$。论文使用：

- $\alpha$：远处面内背景磁化相对 $x$ 轴的方向；
- $\gamma$：两个 meron 核心连线相对 $x$ 轴的方向。

#### 最重要位置

- **Fig. 2(d)，p.4**：整体外观；
- **Fig. 7(c,d)，p.15**：$\alpha$ 与 $\gamma$；
- **Fig. 8(a)，p.15**：纹理、拓扑荷密度和 $m_z$；
- **Sec. 3.2.1，pp.15–17**：完整讨论。

---

## 七、Biskyrmion 与 skyrmionium：两个 skyrmion 的两种组合

### 1. Biskyrmion

#### 组成关系

$$
\boxed{\text{biskyrmion}=\text{两个部分重叠的同号 skyrmion}}.
$$

两个子 skyrmion 通常具有：

- 相同 polarity；
- 相同 vorticity；
- helicity 相差 $\pi$；
- 相同符号的拓扑荷。

对于两个 Bloch skyrmion，可以取

$$
\gamma_1=+\frac{\pi}{2},\qquad
\gamma_2=-\frac{\pi}{2}.
$$

#### 外观

- 两个明显核心；
- 双瓣、花生形或“8”字形；
- 两个子纹理共享同一外部铁磁背景；
- 拓扑荷密度具有两个同号峰。

#### 拓扑荷

若两个子 skyrmion 均为 $+1$，则

$$
N_{\mathrm{biskyrmion}}=+2.
$$

Fig. 2(e) 和 Fig. 8(b) 均采用 $N_{\mathrm{Sk}}=2$。

#### 最重要位置

- **Fig. 2(e)，p.4**：外观；
- **Fig. 6(c)，p.14**：实验图；
- **Fig. 8(b)，p.15**：拓扑荷密度和 $m_z$；
- **Sec. 3.2.2，pp.17–18**。

### 2. Skyrmionium

#### 组成关系

skyrmionium 由内外两个拓扑荷相反的同心子结构组成：

$$
N_{\mathrm{inner}}+N_{\mathrm{outer}}=(+1)+(-1)=0.
$$

论文将其描述为相同 vorticity、相反 polarity 的两个 skyrmion 结构。

#### 外观

- 中心和远处背景方向相同；
- 中间存在一圈反向磁化；
- 径向变化为

$$
+z\rightarrow -z\rightarrow +z
$$

或整体反向；
- 形状像靶心或同心圆环；
- 极角总计变化约 $2\pi$，因此又称 $2\pi$-skyrmion。

#### 拓扑荷

$$
N_{\mathrm{Sk}}=0.
$$

局域拓扑荷密度仍然有限，中央和外环分别具有相反符号。Fig. 8(c) 对这一点展示得最清楚。

整个 skyrmionium 没有唯一的全局 polarity。合适的描述是

$$
N_{\mathrm{inner}}=\pm1,\qquad
N_{\mathrm{outer}}=\mp1.
$$

#### 最重要位置

- **Fig. 2(f)，p.4**：整体外观；
- **Fig. 6(d)，p.14**：与 skyrmionium 相近的 target skyrmion 实验图；
- **Fig. 8(c)，p.15**：局域拓扑荷与环状 $m_z$；
- **Sec. 3.2.3，p.18**。

### 3. 两者的核心区别

| 对象 | 子结构关系 | 拓扑荷组合 | 一眼识别 |
|---|---|---|---|
| biskyrmion | 两个空间上并排、部分重叠的 skyrmion | 同号相加，常为 $\pm2$ | 双核心、花生形 |
| skyrmionium | 两个同心嵌套的反号 skyrmion 区域 | 异号抵消，总和为 $0$ | 同心环、靶心形 |

---

## 八、反铁磁与亚铁磁 skyrmion：改变磁性背景

### 1. Antiferromagnetic skyrmion

#### 组成关系

两个子晶格上的 skyrmion 空间重合，局域磁矩近似反向：

$$
\mathbf m_B(\mathbf r)\approx-\mathbf m_A(\mathbf r).
$$

子晶格拓扑荷为

$$
N_A=+1,\qquad N_B=-1.
$$

#### 外观

- 两套纹理占据相同空间；
- 每一套单独观察都类似 skyrmion；
- 对应磁矩彼此反向；
- 净磁化局域和整体均接近零。

#### 两种拓扑描述

从总磁化 $\mathbf M$ 看：

$$
N_{\mathbf M}=0.
$$

从 Néel order parameter

$$
\mathbf n=\frac{\mathbf m_A-\mathbf m_B}{2}
$$

看：

$$
N_{\mathbf n}=\pm1.
$$

因此，磁化拓扑荷的补偿与反铁磁序参量中的非平凡拓扑可以同时存在。

#### 子晶格参数示例

若 A 子晶格为

$$
p_A=+1,\qquad m_A=+1,\qquad \gamma_A=\gamma,
$$

则反向的 B 子晶格可写成

$$
p_B=-1,\qquad m_B=+1,\qquad \gamma_B=\gamma+\pi.
$$

#### 最重要位置

- **Fig. 2(h)，p.4**：synthetic antiferromagnetic skyrmion；
- **Fig. 6(e)，p.14**：实验 MOKE 图；
- **Fig. 8(d)，p.15**：局域磁化与拓扑荷补偿；
- **Sec. 3.2.4，pp.18–20**。

### 2. Ferrimagnetic skyrmion

#### 组成关系

两个子晶格的磁矩方向相反，大小不同：

$$
|\mathbf M_A|\neq|\mathbf M_B|.
$$

因此

$$
\mathbf M_A+\mathbf M_B\neq0.
$$

#### 外观

- 两套反向纹理空间重合；
- 两个子晶格的磁矩权重不同；
- 总体系保留有限净磁化，因此更容易探测。

两个归一化子晶格纹理可以具有

$$
N_A=+1,\qquad N_B=-1.
$$

磁化补偿和角动量补偿依赖具体温度。论文强调在角动量补偿温度附近，skyrmion Hall effect 可被显著抑制。

#### 最重要位置

- **Fig. 2(g)，p.4**：外观；
- **Fig. 6(f)，p.14**：GdFeCo 中的实验图；
- **Sec. 3.2.5，p.20**。

### 3. 两者的核心区别

| 对象 | 两子晶格关系 | 净磁化 | 拓扑补偿 |
|---|---|---|---|
| antiferromagnetic skyrmion | 方向相反、大小近似相等 | 近似为零 | 总磁化拓扑荷局域和整体抵消 |
| ferrimagnetic skyrmion | 方向相反、大小不同 | 有限 | 子纹理拓扑荷可抵消，磁矩仍不完全抵消 |

---

## 九、三维拓扑纹理：tube、bobber 与 hopfion

### 1. Skyrmion tube

#### 构造关系

$$
\text{二维 skyrmion}
\xrightarrow{\text{沿 }z\text{ 延伸}}
\text{skyrmion tube}.
$$

#### 外观

- 每个垂直于 tube 的横截面都是一个 skyrmion；
- 沿样品厚度方向形成柱状自旋绳；
- helicity 可以沿 tube 保持不变，也可以随 $z$ 改变。

每个横截面仍可定义

$$
p,\quad m,\quad \gamma,\quad N_{\mathrm{Sk}}=mp.
$$

#### 最重要位置

- **Fig. 2(i)，p.4**；
- **Fig. 3(c)，p.4**；
- **Fig. 9(a)，p.17**：emergent field 沿 tube 方向；
- **Sec. 3.3，p.20**。

### 2. Chiral bobber

#### 构造关系

$$
\boxed{\text{chiral bobber}=\text{在 Bloch point 处终止的 skyrmion tube}}.
$$

#### 外观

- 靠近样品表面仍有 skyrmion 截面；
- 沿样品内部逐渐收缩；
- 最后终止于 Bloch point；
- 整体像截短并收尖的管或浮标。

#### 拓扑变化

沿 tube 方向，横截面拓扑荷从

$$
N_{\mathrm{Sk}}=\pm1
$$

变为均匀背景的

$$
N_{\mathrm{Sk}}=0.
$$

这要求磁化场经过三维奇点 Bloch point。

#### 术语区分

- **Bloch skyrmion**：二维 skyrmion 的一种 helicity；
- **Bloch point**：三维磁化方向未定义的奇点。

#### 最重要位置

- **Fig. 2(j)，p.4**；
- **Fig. 6(g)，p.14**：chiral bobber 示意与 Bloch point 实验图；
- **Fig. 10(b)，p.20**：bobber 与 tube 的存储构想；
- **Sec. 3.3.2，p.21**。

### 3. Hopfion

#### 构造关系

$$
\text{skyrmion tube}
\longrightarrow
\text{弯曲}
\longrightarrow
\text{首尾闭合}
\longrightarrow
\text{hopfion}.
$$

#### 外观

- 整体为环面或甜甜圈；
- 局部横截面具有 skyrmion-like 或 bimeron-like 结构；
- 磁化沿环面方向继续扭转；
- 没有开放端点。

#### 三维拓扑量

Hopfion 使用 Hopf invariant：

$$
Q_H=
-\frac{1}{(4\pi)^2}
\int
\mathbf B_{\mathrm{em}}(\mathbf r)\cdot
\mathbf A(\mathbf r)\,d^3r,
$$

其中

$$
\nabla\times\mathbf A=\mathbf B_{\mathrm{em}}.
$$

最简单的 hopfion 中：

- 横截面具有 $\pm1$ 的拓扑荷；
- 磁化沿环面绕行一周时再旋转一次；

于是

$$
Q_H=\pm1.
$$

#### 最重要位置

- **Fig. 2(l)，p.4**：环面外观；
- **Fig. 9(c)，p.17**：局域环形 emergent field；
- **Fig. 10(c)，p.20**：不同取向的 hopfion；
- **Sec. 3.3.3，pp.21–22**。

### 4. 三者的绳结图像

- skyrmion tube：一根贯穿样品的直自旋绳；
- chiral bobber：一根在 Bloch point 处终止的自旋绳；
- hopfion：一根首尾相接的闭合自旋绳。

---

## 十、统一对照表

### 1. 各对象参数与位置总表

| 对象 | 基本组成 | $p$ | $m$ | $\gamma$ | 拓扑量 | 最重要位置 |
|---|---|---:|---:|---:|---:|---|
| Néel skyrmion | 单个完整 skyrmion | $\pm1$ | $+1$ | $0$ 或 $\pi$ | $N=\pm1$ | Fig. 3(a) |
| Bloch skyrmion | 单个完整 skyrmion | $\pm1$ | $+1$ | $\pm\pi/2$ | $N=\pm1$ | Fig. 4(b) |
| Intermediate | 单个完整 skyrmion | $\pm1$ | $+1$ | 任意中间值 | $N=\pm1$ | Fig. 2(b) |
| Antiskyrmion | 反向 vorticity | $\pm1$ | $-1$ | 表示纹理轴取向 | $N=-p$ | Fig. 2(a) |
| Higher-order | 多重绕转 | $\pm1$ | $\pm2,\pm3,\ldots$ | 可变 | $N=mp$ | Fig. 2(c) |
| Meron | 半个 skyrmion | 核心 $\pm1$ | 通常 $\pm1$ | 可变 | $N\approx mp/2$ | Fig. 4(c) |
| Bimeron | meron + antimeron | 无单一全局值 | 无单一全局值 | 用 $\alpha,\gamma$ | $N=\pm1$ | Figs. 2(d), 8(a) |
| Biskyrmion | 两个重叠 skyrmion | 两者相同 | 通常均为 $+1$ | 相差 $\pi$ | $N=\pm2$ | Figs. 2(e), 8(b) |
| Skyrmionium | 内外反号 skyrmion | 无单一值 | 子结构同绕向 | 取决于类型 | $N=0$ | Figs. 2(f), 8(c) |
| AFM skyrmion | 两个反向子晶格纹理 | 子晶格相反 | 通常相同 | 相差 $\pi$ | 总磁化 $0$，Néel 序 $\pm1$ | Figs. 2(h), 8(d) |
| FiM skyrmion | 两个不等强度反向纹理 | 子晶格相反 | 通常相同 | 相差 $\pi$ | 子纹理拓扑荷抵消，净磁化不为零 | Fig. 2(g) |
| Skyrmion tube | skyrmion 沿 $z$ 延伸 | 看横截面 | 看横截面 | 可沿 $z$ 变化 | 每个截面通常 $\pm1$ | Figs. 2(i), 3(c) |
| Chiral bobber | 中途终止的 tube | 无全局值 | 无全局值 | 无全局值 | 截面由 $\pm1$ 变到 $0$ | Fig. 2(j) |
| Hopfion | 闭合成环的 tube | 不适用 | 不适用 | 不适用 | 最简单 $Q_H=\pm1$ | Fig. 2(l) |

### 2. Fig. 2(a–l) 外观对照

| Panel | 对象 | 图中给出的拓扑信息 | 一眼识别 |
|---|---|---|---|
| Fig. 2(a) | antiskyrmion | $m=-1,\ N=-1$ | 径向与切向特征交替，明显各向异性 |
| Fig. 2(b) | intermediate skyrmion | $\gamma=\pi/4,\ N=1$ | 圆对称，箭头介于径向与切向 |
| Fig. 2(c) | higher-order skyrmion | $N=2$ | 面内磁化绕转多次 |
| Fig. 2(d) | bimeron | $N=-1$ | 面内背景，两个相反的面外核心 |
| Fig. 2(e) | biskyrmion | $N=2$ | 双核心、花生形 |
| Fig. 2(f) | skyrmionium | $N=0$ | 同心环、靶心结构 |
| Fig. 2(g) | ferrimagnetic skyrmion | 子纹理拓扑荷补偿 | 两套反向纹理强度不同 |
| Fig. 2(h) | antiferromagnetic skyrmion | 子纹理拓扑荷补偿 | 两套重合且反向的纹理 |
| Fig. 2(i) | skyrmion tube | 横截面为 skyrmion | 贯穿样品的柱状纹理 |
| Fig. 2(j) | chiral bobber | tube 在 Bloch point 终止 | 截短并收尖的 skyrmion 管 |
| Fig. 2(k) | Bloch–anti-Bloch points | 三维磁化奇点对 | 两个 hedgehog 型球状奇点 |
| Fig. 2(l) | hopfion | 使用 $Q_H$ 表征 | 闭合甜甜圈结构 |

### 3. 组合关系总表

| 对象 | 构造方式 | 子结构拓扑荷 | 总拓扑荷/拓扑量 |
|---|---|---|---|
| meron | 半个 skyrmion | 单个 $\pm1/2$ | $\pm1/2$ |
| bimeron | meron + antimeron | 同号 $\pm1/2$ 与 $\pm1/2$ | $\pm1$ |
| biskyrmion | 两个同号 skyrmion 部分重叠 | $\pm1$ 与 $\pm1$ | $\pm2$ |
| skyrmionium | 内外反号 skyrmion 同心嵌套 | $+1$ 与 $-1$ | $0$ |
| AFM skyrmion | 两个反向子晶格 skyrmion | $+1$ 与 $-1$ | 总磁化为 $0$；Néel 序为 $\pm1$ |
| FiM skyrmion | 两个不等强度反向子晶格 skyrmion | $+1$ 与 $-1$ | 子纹理荷补偿；净磁化有限 |
| chiral bobber | 终止的 skyrmion tube | 横截面从 $\pm1$ 变为 $0$ | Bloch point 连接两类截面 |
| hopfion | 闭合的 skyrmion tube | 局部截面通常为 $\pm1$ | Hopf invariant $Q_H$ |

---

## 十一、最容易混淆的概念

### 1. Néel/Bloch 与 skyrmion/antiskyrmion

- Néel、Bloch、intermediate 主要描述 helicity；
- skyrmion、antiskyrmion 主要区分 vorticity 和空间对称性。

因此，一个对象的命名可以同时包含不同层次的信息，例如“Néel-type skyrmion”。antiskyrmion 内部则同时包含 Néel-like 和 Bloch-like 方向截面。

### 2. Meron、antimeron 与 antiskyrmion

- antimeron：半 skyrmion，vorticity 与 meron 相反；
- antiskyrmion：完整球面覆盖的各向异性纹理，典型 $m=-1$；
- 二者的前缀 “anti” 都涉及绕转方向，但覆盖范围和整体外观不同。

### 3. Bimeron 与 biskyrmion

- bimeron：两个半整数拓扑单元，远处背景位于面内；
- biskyrmion：两个完整 skyrmion 部分重叠，远处背景通常面外磁化。

### 4. Skyrmionium 与 biskyrmion

- biskyrmion：两个核心并排，同号拓扑荷相加；
- skyrmionium：同心圆环，反号拓扑荷抵消。

### 5. Bloch skyrmion 与 Bloch point

- Bloch skyrmion：二维纹理的一种 helicity，面内磁矩沿切向；
- Bloch point：三维磁化奇点，磁化方向在一点处无法定义。

### 6. 反铁磁 skyrmion 的“总拓扑荷为零”

该表述依赖使用的序参量：

- 用总磁化描述，两子晶格贡献抵消；
- 用 Néel order parameter 描述，仍有 $\pm1$ 的非平凡拓扑。

---

## 十二、这篇综述的主线与物理价值

### 1. 传统 skyrmion 提供参照系

传统 skyrmion 同时带来三类重要性质：

- 非平凡实空间拓扑；
- 小尺寸下的稳定性；
- emergent electrodynamics，包括 topological Hall effect 与 skyrmion Hall effect。

这些性质构成评价替代磁纹理的共同坐标。

### 2. 替代纹理的设计逻辑

替代磁纹理通常沿以下方向优化：

- 调整 helicity 或纹理各向异性，改变电流驱动力方向；
- 组合相反拓扑荷，抵消整体 gyroscopic force；
- 使用反铁磁或亚铁磁背景，降低净磁化和横向运动；
- 构造三维纹理，使 emergent field、净磁化和稳定磁场进入不同空间方向。

### 3. 与器件应用的关系

- antiskyrmion、特定 helicity 的 skyrmion 和 bimeron 可以通过各向异性驱动力实现特定方向的直线运动；
- skyrmionium 与反铁磁 skyrmion 通过拓扑荷补偿抑制整体 skyrmion Hall effect；
- bimeron 与 hopfion 中 emergent field、净磁化和外磁场方向可以分离，有利于区分不同 Hall 响应；
- skyrmion tube/chiral bobber、skyrmion/antiskyrmion 等不同对象可分别编码两种信息状态。

当前笔记主要保留这些应用结论与分类之间的联系，具体 LLG、Thiele 方程和 Hall 响应推导可在后续专题中单独展开。

---

## 十三、对我的价值与可调用内容

### 1. 概念调用

这篇综述适合用于快速定义和区分：

- skyrmion、meron、antiskyrmion；
- Néel、Bloch 和 intermediate helicity；
- bimeron、biskyrmion、skyrmionium；
- 反铁磁和亚铁磁 skyrmion；
- skyrmion tube、chiral bobber、hopfion。

### 2. 图像调用

- **Fig. 1**：引用拓扑磁纹理的总分类框架；
- **Fig. 2**：作为全部代表性外观的图鉴；
- **Fig. 3**：解释二维 skyrmion 的球面覆盖与 tube 延伸；
- **Fig. 4(c)**：解释 meron–antimeron lattice；
- **Fig. 8**：解释复合纹理中拓扑荷密度如何相加或抵消；
- **Fig. 9**：解释 emergent field 与净磁化方向的关系；
- **Fig. 10**：解释不同拓扑对象编码信息的器件构想。

### 3. 与当前研究问题的联系

对于“极性 meron 与磁性 skyrmion 耦合”“多铁性拓扑纹理”等问题，这篇综述提供磁性侧的基础语言：

- meron 与 skyrmion 的完整/半球覆盖关系；
- 拓扑荷、polarity、vorticity、helicity 的定义；
- 多个纹理组合后拓扑荷的相加与抵消；
- 二维和三维拓扑磁纹理的分类边界。

---

## 十四、最终物理图像

1. **Skyrmion**：中心与背景反向，中间自旋连续翻转，完整覆盖一次自旋球面。
2. **Néel、Bloch、intermediate**：拓扑荷可以相同，区别主要在面内磁化沿径向、切向或介于两者之间。
3. **Antiskyrmion**：vorticity 改变，纹理具有明显各向异性。
4. **Meron**：半个 skyrmion；bimeron 由 meron 与 antimeron 组成，并可视为面内背景中的 skyrmion。
5. **Biskyrmion**：两个同号完整 skyrmion 部分重叠，常有 $|N|=2$。
6. **Skyrmionium**：内外反号子结构同心嵌套，总拓扑荷为零。
7. **AFM/FiM skyrmion**：两个反向子晶格纹理重合，区别在磁矩是否完全补偿。
8. **Skyrmion tube、chiral bobber、hopfion**：分别对应贯穿的自旋绳、在奇点处终止的自旋绳和首尾闭合的自旋绳。

最适合长期保留的一条总主线是：

$$
\boxed{
\text{完整或半个球面覆盖}
\rightarrow
\text{改变绕转参数}
\rightarrow
\text{组合多个子纹理}
\rightarrow
\text{改变磁性背景}
\rightarrow
\text{扩展到三维}
}
$$

---

## 后续查证

1. meron 的 $N\approx mp/2$ 属于理想半球覆盖下的推广表达；后续如需严格处理边界条件，应回到具体磁化参数化重新积分。
2. antiskyrmion 的 helicity 与普通圆对称 skyrmion 的 helicity 含义不同，做张量或动力学推导时需要采用论文 Sec. 3.1.2 的具体定义。
3. biskyrmion 的部分早期 LTEM 实验解释在本文中仍有争议，可能受到样品倾斜造成的成像伪影影响。
4. 本综述覆盖的研究进展主要截至 2020 年，涉及当前实验状态时需要补充近年文献。
5. 后续若继续研究应用问题，可单独整理 DMI 稳定机制、LLG/Thiele 方程、topological Hall effect 与 skyrmion Hall effect。

---

# 过程稿归档

## 快速建档原稿

<details>
<summary>展开 A：重要文献快速建档</summary>

## 文献信息

- **标题**：Beyond skyrmions: Review and perspectives of alternative magnetic quasiparticles
- **作者**：Börge Göbel, Ingrid Mertig, Oleg A. Tretiakov
- **期刊与年份**：Physics Reports 895, 1–28 (2021)
- **DOI**：10.1016/j.physrep.2020.10.001
- **文章类型**：综述
- **本次阅读依据**：正文 PDF；未发现理解主线所必需的补充材料

## 一句话总结与研究对象

本文建立了一套超越传统磁性 skyrmion 的拓扑磁织构分类框架，并围绕稳定机制、拓扑电输运和电流驱动动力学，比较 antiskyrmion、bimeron、skyrmionium、反铁磁 skyrmion、chiral bobber、hopfion 等准粒子的潜在优势。

研究对象是实空间非共线磁织构及其在自旋电子学，尤其是 racetrack memory 中的应用。

## 旧问题与新贡献

传统 skyrmion 具有小尺寸和拓扑稳定性，但有限拓扑荷会产生 skyrmion Hall effect。电流驱动时，skyrmion 会横向偏转并靠近轨道边缘，造成钉扎或信息丢失。不同替代磁织构近年来快速出现，此前缺少统一的分类与横向比较。

本文作为综述的主要贡献包括：

1. **提出三级分类框架**：将磁织构分为基本激发、基本激发的变体，以及二维或三维扩展。
2. **统一比较关键物理量**：以拓扑荷、磁性背景、组成方式和空间维度组织不同准粒子。
3. **用 emergent electrodynamics 评价器件潜力**：重点比较 topological Hall effect、skyrmion Hall effect 和 SOT/STT 驱动。
4. **指出若干优势对象**：反铁磁 skyrmion 可实现高速直线运动；antiskyrmion、特定 helicity 的 skyrmion 和 bimeron 可通过驱动力方向补偿横向力；bimeron 与 hopfion 有望分离普通、反常和拓扑 Hall 信号。

## 核心证据与关键位置

- **Fig. 1，p.3**：全文分类总图。基本激发包括 skyrmion 和 meron；变体来自多个子粒子组合或磁性背景改变；扩展包括二维晶格和三维对象。
- **Fig. 2，p.4**：集中展示主要磁织构，是建立直观区别的入口。
- **Eqs. (1)–(7)，p.5**：给出拓扑荷密度及 skyrmion 的三个主要表征量：polarity $p$、vorticity $m$、helicity $\gamma$。对常规 skyrmion，有 $N_{\mathrm{Sk}}=mp$。
- **Eqs. (23)–(25)，p.10**：Thiele 方程将磁织构压缩为质点运动，说明 gyroscopic force 与 $N_{\mathrm{Sk}}$ 直接相关，是理解 skyrmion Hall effect 的核心。
- **Fig. 7，p.15**：即使 $N_{\mathrm{Sk}}=1$，特定 helicity 或取向的 skyrmion、bimeron 和 antiskyrmion 仍可在 SOT 下直线运动，因为驱动力的横向分量补偿了 gyroscopic force。
- **Fig. 8，p.15**：对比复合织构的拓扑荷。skyrmionium 和反铁磁 skyrmion 的总磁化拓扑荷相互抵消，因此整体横向运动受到抑制。
- **Fig. 9，p.17**：bimeron 与 hopfion 中 emergent field、净磁化和稳定磁场方向不再平行，可使不同 Hall 响应进入不同电阻率张量分量。
- **Fig. 10，p.20**：总结三类信息存储方案，包括 skyrmion/antiskyrmion、skyrmion tube/chiral bobber 和不同取向的 hopfion。
- **结论，pp.22–23**：作者将反铁磁 skyrmion 视为最有希望的候选之一，同时强调 antiskyrmion 以及用两种不同准粒子分别编码“0/1”的方案。

## 对用户的潜在价值与引用方式

这篇综述和非线性光学、堆叠铁电的直接联系较弱，但对理解磁性 skyrmion、meron 及其耦合体系很有价值。

- 可用于建立 **skyrmion、antiskyrmion、meron、bimeron、skyrmionium** 的概念边界。
- 可用于解释拓扑荷、helicity、vorticity 以及 emergent magnetic field 的关系。
- 可作为讨论“极性 meron 与磁性 skyrmion 耦合”“多铁性拓扑织构”时的磁性背景文献。
- 可引用其 Fig. 1 的分类框架，说明替代拓扑磁准粒子的主要构造路径。
- 可引用 Thiele 方程部分，支持“有限拓扑荷通常导致横向运动，但织构对称性和驱动力张量也会改变实际轨迹”的观点。
- 由于本文覆盖进展主要截至 2020 年，不宜单独用于概括当前最新实验状态。

## 阅读优先级与建议去向

**结构阅读：建议移动到 `1_处理中`。**

它是一篇适合作为概念地图和公式索引的综述，和当前 meron、skyrmion 及多铁耦合问题直接相关；没有必要逐段精读全部材料案例。

**下一步动作**：先精读 Fig. 1、Fig. 2 与 Sec. 2.1，建立拓扑荷、polarity、vorticity、helicity 的定义；随后阅读 Sec. 3.1.2、3.2.1、3.2.3 和 3.2.4，重点比较 antiskyrmion、bimeron、skyrmionium 与反铁磁 skyrmion。

</details>

## 处理中草稿

<details>
<summary>展开 B：Skyrmion 及相关拓扑磁纹理的分类、几何参数与外观</summary>

<!-- B-SUMMARY: 2026-08-06 | 范围：Skyrmion 及相关拓扑磁纹理的分类、几何参数、外观与原文图像位置 -->

### Polarity、vorticity、helicity 与拓扑荷

#### 磁化方向的角度表示

二维归一化磁化场可写为

$$
\mathbf m(\mathbf r)=
\begin{pmatrix}
\sin\theta\cos\Phi\\
\sin\theta\sin\Phi\\
\cos\theta
\end{pmatrix},
$$

其中 $\theta$ 决定面外分量，$\Phi$ 是磁矩在平面内的方位角，实空间位置写作 $\mathbf r=r(\cos\phi,\sin\phi)$。轴对称纹理通常满足 $\theta=\theta(r)$、$\Phi=\Phi(\phi)$。

#### 拓扑荷密度与总拓扑荷

$$
N_{\mathrm{Sk}}=\int n_{\mathrm{Sk}}(\mathbf r)\,d^2r,
$$

$$
n_{\mathrm{Sk}}(\mathbf r)=
\frac{1}{4\pi}
\mathbf m(\mathbf r)\cdot
\left[
\frac{\partial\mathbf m}{\partial x}
\times
\frac{\partial\mathbf m}{\partial y}
\right].
$$

$N_{\mathrm{Sk}}$ 表示二维磁化场覆盖自旋单位球面的次数和方向。

#### Polarity

$$
p=
-\frac12
\left[
\cos\theta(\infty)-\cos\theta(0)
\right].
$$

中心朝 $+z$、背景朝 $-z$ 时 $p=+1$；整体反转时 $p=-1$。

#### Vorticity

$$
m=
\frac{\Phi(2\pi)-\Phi(0)}{2\pi}.
$$

$m$ 描述沿实空间绕中心一周时，面内磁化旋转的圈数和方向。

#### Helicity

$$
\Phi(\phi)=m\phi+\gamma.
$$

对 $m=+1$ 的圆对称 skyrmion，$\gamma=0,\pi$ 对应 Néel 型，$\gamma=\pm\pi/2$ 对应 Bloch 型，其他角度对应 intermediate-helicity skyrmion。

#### 三个参数与拓扑荷

$$
N_{\mathrm{Sk}}=mp.
$$

改变 $p$ 或 $m$ 会改变拓扑荷；改变 $\gamma$ 不改变拓扑荷。理想 meron 可近似写作 $N_{\mathrm{meron}}\approx mp/2$。

### 所有纹理的总体关系

- 基本二维单元：skyrmion 与 meron。
- 改变内部绕转：Néel、Bloch、intermediate、antiskyrmion、higher-order。
- 组合或改变背景：bimeron、biskyrmion、skyrmionium、AFM/FiM skyrmion。
- 向三维延伸：skyrmion tube、chiral bobber、hopfion。

### Skyrmion、Néel、Bloch 与 intermediate

- 一般 skyrmion：中心与背景相反，中间磁化连续翻转，完整覆盖一次自旋球面。重要位置为 Fig. 3(a–c) 与 Sec. 2.1。
- Néel skyrmion：面内磁化沿径向；Fig. 3(a) 采用 $p=+1,m=+1,\gamma=0,N=+1$。
- Bloch skyrmion：面内磁化沿切向；Fig. 4(b) 给出 $m=+1,\gamma=-\pi/2$ 的 Bloch skyrmion lattice。
- intermediate：面内磁化介于径向与切向；Fig. 2(b) 给出 $\gamma=\pi/4,N=1$。

### Antiskyrmion

Antiskyrmion 具有 $m=-1$，沿不同空间方向分别呈现 Néel-like 和 Bloch-like 截面，纹理具有明显各向异性。Fig. 2(a) 给出 $m=-1,N=-1$；Sec. 3.1.2 讨论其几何与 DMI；Fig. 6(a) 是实验 LTEM 图；Fig. 7(e,f) 展示特定取向下的直线运动。

### Meron 与 bimeron

Meron 只覆盖半个自旋球面，中心为面外磁化，外围转入面内，典型拓扑荷为 $\pm1/2$。Fig. 4(c) 给出 meron–antimeron lattice。Bimeron 由 meron 与 antimeron 组成，也可以理解为面内磁化背景中的 skyrmion。Fig. 2(d) 和 Fig. 8(a) 分别展示 $N=-1$ 与 $N=+1$ 的 bimeron；Fig. 7(c,d) 定义背景磁化方向 $\alpha$ 和双核心连线方向 $\gamma$。

### Biskyrmion

Biskyrmion 由两个部分重叠、拓扑荷同号的 skyrmion 组成，两个子纹理通常具有相同 polarity 和 vorticity、相差 $\pi$ 的 helicity。外观为双核心或花生形。Fig. 2(e) 和 Fig. 8(b) 给出 $N=2$。

### Skyrmionium

Skyrmionium 由内外两个拓扑荷相反的同心子结构组成，中心和远处背景方向相同，中间存在反向圆环。径向磁化经历 $+z\rightarrow-z\rightarrow+z$，因此也称 $2\pi$-skyrmion。总拓扑荷为零，局域拓扑荷密度在中心和外环分别取相反符号。重要位置为 Fig. 2(f)、Fig. 8(c) 与 Sec. 3.2.3。

### 反铁磁与亚铁磁 skyrmion

反铁磁 skyrmion 由两个空间重合、磁矩反向的子晶格 skyrmion 构成。总磁化拓扑荷抵消，Néel order parameter 仍具有 $\pm1$ 的拓扑荷。亚铁磁 skyrmion 的两个子晶格磁矩大小不同，因此净磁化有限。重要位置为 Fig. 2(g,h)、Fig. 6(e,f)、Fig. 8(d) 与 Secs. 3.2.4–3.2.5。

### 三维纹理

- Skyrmion tube：二维 skyrmion 沿第三维延伸，见 Figs. 2(i)、3(c)、9(a)。
- Chiral bobber：在 Bloch point 处终止的 skyrmion tube，见 Figs. 2(j)、6(g)、10(b)。
- Hopfion：闭合成环的 skyrmion tube，使用 Hopf invariant $Q_H$ 描述，见 Figs. 2(l)、9(c)、10(c)。

### 参数总表

| 对象 | 基本组成 | $p$ | $m$ | $\gamma$ | 拓扑量 | 最重要位置 |
|---|---|---:|---:|---:|---:|---|
| Néel skyrmion | 单个完整 skyrmion | $\pm1$ | $+1$ | $0$ 或 $\pi$ | $N=\pm1$ | Fig. 3(a) |
| Bloch skyrmion | 单个完整 skyrmion | $\pm1$ | $+1$ | $\pm\pi/2$ | $N=\pm1$ | Fig. 4(b) |
| Intermediate | 单个完整 skyrmion | $\pm1$ | $+1$ | 任意中间值 | $N=\pm1$ | Fig. 2(b) |
| Antiskyrmion | 反向 vorticity | $\pm1$ | $-1$ | 表示纹理轴取向 | $N=-p$ | Fig. 2(a) |
| Higher-order | 多重绕转 | $\pm1$ | $\pm2,\pm3,\ldots$ | 可变 | $N=mp$ | Fig. 2(c) |
| Meron | 半个 skyrmion | 核心 $\pm1$ | 通常 $\pm1$ | 可变 | $N\approx mp/2$ | Fig. 4(c) |
| Bimeron | meron + antimeron | 无单一全局值 | 无单一全局值 | 用 $\alpha,\gamma$ | $N=\pm1$ | Figs. 2(d), 8(a) |
| Biskyrmion | 两个重叠 skyrmion | 两者相同 | 通常均为 $+1$ | 相差 $\pi$ | $N=\pm2$ | Figs. 2(e), 8(b) |
| Skyrmionium | 内外反号 skyrmion | 无单一值 | 子结构同绕向 | 取决于类型 | $N=0$ | Figs. 2(f), 8(c) |
| AFM skyrmion | 两个反向子晶格纹理 | 子晶格相反 | 通常相同 | 相差 $\pi$ | 总磁化 $0$，Néel 序 $\pm1$ | Figs. 2(h), 8(d) |
| FiM skyrmion | 两个不等强度反向纹理 | 子晶格相反 | 通常相同 | 相差 $\pi$ | 子纹理荷抵消，净磁化不为零 | Fig. 2(g) |
| Skyrmion tube | skyrmion 沿 $z$ 延伸 | 看横截面 | 看横截面 | 可沿 $z$ 变化 | 每个截面通常 $\pm1$ | Figs. 2(i), 3(c) |
| Chiral bobber | 中途终止的 tube | 无全局值 | 无全局值 | 无全局值 | 截面由 $\pm1$ 变到 $0$ | Fig. 2(j) |
| Hopfion | 闭合成环的 tube | 不适用 | 不适用 | 不适用 | 最简单 $Q_H=\pm1$ | Fig. 2(l) |

### Fig. 2(a–l) 外观对照

| Panel | 对象 | 图中给出的拓扑信息 | 一眼识别 |
|---|---|---|---|
| Fig. 2(a) | antiskyrmion | $m=-1,\ N=-1$ | 径向与切向特征交替、明显各向异性 |
| Fig. 2(b) | intermediate skyrmion | $\gamma=\pi/4,\ N=1$ | 圆对称，箭头介于径向和切向 |
| Fig. 2(c) | higher-order skyrmion | $N=2$ | 面内磁化绕转多次 |
| Fig. 2(d) | bimeron | $N=-1$ | 面内背景、两个相反的面外核心 |
| Fig. 2(e) | biskyrmion | $N=2$ | 双核心、花生形 |
| Fig. 2(f) | skyrmionium | $N=0$ | 同心环、靶心结构 |
| Fig. 2(g) | ferrimagnetic skyrmion | 子纹理拓扑荷补偿 | 两套反向纹理强度不同 |
| Fig. 2(h) | antiferromagnetic skyrmion | 子纹理拓扑荷补偿 | 两套重合且反向的纹理 |
| Fig. 2(i) | skyrmion tube | 横截面为 skyrmion | 贯穿样品的柱状纹理 |
| Fig. 2(j) | chiral bobber | tube 在 Bloch point 终止 | 截短并收尖的 skyrmion 管 |
| Fig. 2(k) | Bloch–anti-Bloch points | 三维磁化奇点对 | 两个 hedgehog 型球状奇点 |
| Fig. 2(l) | hopfion | 使用 $Q_H$ 表征 | 闭合甜甜圈结构 |

### 最终物理图像

1. Skyrmion：中心与背景反向，中间自旋连续翻转，完整覆盖一次自旋球面。
2. Néel、Bloch、intermediate：拓扑荷可以相同，区别在面内磁化沿径向、沿切向或介于二者之间。
3. Antiskyrmion：面内绕转方向改变，纹理表现出各向异性。
4. Meron：半个 skyrmion；bimeron 是 meron 与 antimeron 组合形成的面内 skyrmion。
5. Biskyrmion、skyrmionium、AFM/FiM skyrmion：都可理解为两个 skyrmion 子结构的组合，区别在拓扑荷相加或抵消、两个纹理是否空间分离，以及两个子晶格是否等强度。
6. Skyrmion tube、chiral bobber、hopfion：分别对应拉直的 skyrmion 绳、在 Bloch point 处终止的绳，以及首尾闭合的绳。

</details>



## V50 发布说明

- **反铁磁 skyrmion**：A/B 两个子晶格在主图中拉开显示；两层使用同一 Néel-order 方向色标与相同显示强度，真实反平行关系只由箭头方向表达。
- **亚铁磁 skyrmion**：A/B 使用同一方向色标；磁矩幅值差异只由箭头长度表达。本页采用教学比例 $|m_B|\approx0.70|m_A|$，并直接显示残余净磁化 $M_{net}=m_A+m_B$，对应 $|M_{net}|\approx0.30|m_A|$。这些比例用于可视化，不是材料通用常数。
- **Biskyrmion**：适度增大两个局域核心的分离并收紧权重，使双核心更多由纹理本身显现，而不是依赖红/蓝辅助标记。
- **导出 PNG**：使用完整英文预设名称，例如 `Ferrimagnetic_skyrmion.png`、`Neel_skyrmion_outward.png`，不再暴露内部 key。
- **中文发布文案**：右侧参数值、资源区与 Source focus 统一为中文优先，保留必要英文科学术语用于检索。
