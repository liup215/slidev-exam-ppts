# Chapter 7: Gene Expression Control 基因表达调控

## 学习目标

- 理解原核生物操纵子模型（lac 操纵子）
- 掌握真核生物基因表达调控的层次
- 了解转录因子与染色质重塑的作用
- 理解表观遗传学基础

---

## 7.1 基因表达调控概述

基因表达的层次：

$$\text{DNA} \xrightarrow{\text{转录}} \text{mRNA} \xrightarrow{\text{翻译}} \text{蛋白质} \xrightarrow{\text{修饰}} \text{功能蛋白}$$

调控可发生在：
1. **转录水平**（最主要）
2. **转录后水平**（RNA 剪接、mRNA 稳定性）
3. **翻译水平**（翻译效率）
4. **翻译后水平**（蛋白质修饰、降解）

---

## 7.2 原核生物：Lac 操纵子

*E. coli* 乳糖操纵子（lac operon）是调控的经典模型：

```
DNA: ─[启动子 P]─[操纵基因 O]─[lacZ]─[lacY]─[lacA]─
                      ↑
              阻遏蛋白结合位点
```

### 负调控（无乳糖时）

1. **阻遏蛋白（Repressor）** 结合操纵基因
2. RNA 聚合酶无法通过，转录**阻断**
3. lacZ（β-半乳糖苷酶）等酶**不表达**

### 乳糖存在时

1. 乳糖（实为 **异乳糖，allolactose**）作为**诱导物（inducer）**
2. 诱导物结合阻遏蛋白 → 阻遏蛋白构象改变
3. 阻遏蛋白脱离操纵基因 → 转录**开启**

### 葡萄糖与 cAMP 的正调控

$$[\text{葡萄糖}] \downarrow \Rightarrow [\text{cAMP}] \uparrow \Rightarrow \text{CAP-cAMP} \text{ 结合启动子} \Rightarrow \text{转录增强}$$

| 葡萄糖 | 乳糖 | cAMP | 操纵子状态 |
|--------|------|------|-----------|
| + | - | 低 | 关闭 |
| - | - | 高 | 关闭（阻遏蛋白结合） |
| + | + | 低 | 低水平转录 |
| - | + | 高 | **最高水平转录** |

---

## 7.3 真核生物转录调控

### 顺式调控元件

| 元件 | 位置 | 功能 |
|------|------|------|
| 启动子（Promoter） | 转录起始位点上游 | TATA box 等，RNA pol II 结合 |
| 增强子（Enhancer） | 可在基因远端 | 提高转录效率（可达10³× 以上） |
| 沉默子（Silencer） | 可变 | 抑制转录 |

增强子与启动子相互作用：

```
增强子 ←─ DNA 环 ─→ 启动子
  ↑                    ↑
转录因子              TATA-box + RNA pol II
```

### 转录因子 (Transcription Factors)

- **通用转录因子（GTF）**：TFIIA、TFIIB、TFIID 等，形成转录起始复合体
- **特异转录因子**：与增强子/沉默子结合，调节特定基因

转录因子常见功能域：

```python
# 转录因子结构域示例（伪代码）
class TranscriptionFactor:
    def __init__(self):
        self.dna_binding_domain  = "识别特定 DNA 序列"
        self.activation_domain   = "激活转录机器"
        self.dimerization_domain = "与其他 TF 形成二聚体"
```

---

## 7.4 染色质重塑与组蛋白修饰

染色质结构影响转录可及性：

$$\text{异染色质（密实）} \rightleftharpoons \text{常染色质（松散）}$$

### 组蛋白修饰

| 修饰类型 | 位置 | 效果 |
|---------|------|------|
| 乙酰化（Acetylation） | H3K9ac, H3K27ac | 激活转录（松散染色质） |
| 甲基化（Methylation） | H3K4me3（激活）/ H3K27me3（抑制） | 双向调控 |
| 磷酸化（Phosphorylation） | H3S10ph | 染色体凝缩 |

### DNA 甲基化

$$\text{胞嘧啶（C）} + \text{甲基基团} \rightarrow 5\text{-甲基胞嘧啶（}^5\text{mC）}$$

- 发生在 **CpG 二核苷酸**（$5'-CG-3'$）
- 启动子区域 CpG 甲基化 → **基因沉默**
- 表观遗传标记，可在细胞分裂时**遗传**

---

## 7.5 转录后调控

### RNA 剪接（Alternative Splicing）

$$\text{Pre-mRNA} \xrightarrow{\text{剪接体}} \text{成熟 mRNA（可有多种异构体）}$$

一个基因可产生多种蛋白质异构体（isoforms），增加蛋白质组多样性。

### microRNA (miRNA)

miRNA 调控机制：

1. **miRNA 前体**转录 → 茎环结构
2. Dicer 酶切割 → 成熟 miRNA（~22 nt）
3. 与 RISC 复合物结合
4. 靶向 **互补 mRNA** 的 3'-UTR
5. mRNA **降解**或**翻译抑制**

$$\text{miRNA 互补性} \begin{cases} \text{完全互补} \rightarrow \text{mRNA 切割} \\ \text{不完全互补} \rightarrow \text{翻译抑制} \end{cases}$$

---

## 7.6 细胞分化与基因表达

> 所有体细胞含有**相同的基因组**，但不同细胞表达不同的基因子集。

细胞分化中的关键转录因子：

- **MyoD**：肌肉细胞分化（激活肌肉特异基因）
- **Oct4、Sox2、Klf4、c-Myc**：诱导多能干细胞（iPSC）重编程

---

## 考点整理

1. Lac 操纵子：**乳糖（allolactose）** 是诱导物，非乳糖本身
2. 增强子可在**远端**（数千 bp 外）发挥作用，通过 DNA 弯曲与启动子相互作用
3. 组蛋白乙酰化 → 正电荷减弱 → DNA 结合力↓ → 染色质松散 → 转录激活
4. miRNA 通过 **RISC** 发挥功能，靶向 mRNA 的 **3'-UTR**

---

*本笔记对应生物竞赛《细胞生物学》第 7 章*
