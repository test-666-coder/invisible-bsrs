#set page(width: 13.333in, height: 7.5in, margin: 0pt, fill: rgb("#F7F0ED"))
#set text(font: ("PingFang TC", "Heiti TC", "Arial Unicode MS"), fill: rgb("#251D1B"), lang: "zh", size: 17pt)
#set par(leading: 0.72em)

#let wine = rgb("#8E1F1F")
#let red = rgb("#C12720")
#let ink = rgb("#251D1B")
#let cream = rgb("#F7F0ED")
#let blush = rgb("#EEDDD8")
#let sand = rgb("#E6DED4")
#let gold = rgb("#C89A35")
#let muted = rgb("#756965")

// 16:9 layout grid: 0.58in side margins, 1.35in content start,
// and a protected footer baseline at 7.26in.
#let margin-x = 0.58in
#let content-w = 12.173in
#let content-y = 1.35in
#let gap = 0.18in

#let footer(n) = place(
  bottom + left,
  dx: 0.46in,
  dy: -0.24in,
  text(size: 8pt, fill: muted)[Invisible BSRS｜Build with AI Hackathon],
) + place(
  bottom + right,
  dx: -0.46in,
  dy: -0.24in,
  text(size: 9pt, fill: muted)[#n],
)

#let brand() = place(top + right, dx: -0.46in, dy: 0.31in)[
  #align(right)[
    #text(size: 9pt, weight: "bold", fill: wine)[INVISIBLE]
    #linebreak()
    #text(size: 6.5pt, tracking: 1.6pt, fill: wine)[BSRS]
  ]
]

#let head(no, title, en, n) = {
  place(top + left, dx: 0.46in, dy: 0.42in)[
    #grid(columns: (0.28in, auto), column-gutter: 0.12in,
      line(length: 0.28in, stroke: 1.2pt + ink),
      block[
        #text(size: 25pt, weight: "bold", fill: ink)[#no、#title]
        #linebreak()
        #text(size: 7.2pt, weight: "bold", tracking: 1.4pt, fill: muted)[#en]
      ]
    )
  ]
  brand()
}

#let panel(body, fill: white, height: auto, inset: 18pt, radius: 7pt, stroke: none) = block(
  width: 100%, height: height, fill: fill, inset: inset, radius: radius, stroke: stroke, body
)

#let deck-grid(..args) = block(width: content-w, grid(..args))

#let tag(body, fill: red) = box(fill: fill, radius: 12pt, inset: (x: 14pt, y: 6pt))[
  #text(size: 12pt, fill: white, weight: "bold")[#body]
]

#let bullet(body) = grid(columns: (9pt, 1fr), column-gutter: 8pt,
  circle(radius: 3.2pt, fill: wine),
  text(size: 15pt)[#body]
)

// 01 — title
#place(left + top, dx: 0.62in, dy: 0.58in)[
  #text(size: 11pt, tracking: 2pt, fill: wine, weight: "bold")[BUILD WITH AI HACKATHON]
]
#place(left + horizon, dx: 0.72in, dy: -0.42in)[
  #text(size: 48pt, weight: "bold", fill: wine)[隱形溫度計]
  #linebreak()
  #text(size: 17pt, tracking: 3pt, fill: wine)[INVISIBLE BSRS]
  #v(0.34in)
  #text(size: 24pt, weight: "bold", fill: ink)[用傾聽取代填表，讓求救訊號被看見]
]
#place(right + horizon, dx: -0.72in, dy: -0.12in)[
  #box(width: 3.5in, height: 3.5in, fill: wine, radius: 50%)[
    #align(center + horizon)[
      #text(size: 64pt, weight: "bold", fill: white)[05]
      #linebreak()
      #text(size: 12pt, tracking: 2pt, fill: white)[SIGNALS · ONE CONVERSATION]
    ]
  ]
]
#place(bottom + left, dx: 0.72in, dy: -0.52in)[
  #text(size: 11pt, fill: muted)[醫療對話情緒解析 × BSRS-5 評估草稿 × 人工確認]
]
#pagebreak()

// 02 — current state
#head("壹", "現況分析", "THE SIGNALS ARE ALREADY IN THE CONVERSATION", 2)
#place(left + top, dx: margin-x, dy: content-y)[
  #deck-grid(columns: (1fr, 1fr, 1fr), gutter: gap,
    ..(("1", "低報風險", "防衛、污名或缺乏信任，讓真正的困擾不一定出現在量表上。"),
       ("2", "時間有限", "醫療人員同時要建立關係、理解主訴，也要辨識心理風險。"),
       ("3", "線索分散", "失眠、易怒、自我否定常藏在自然敘述裡，容易被匆忙略過。"))
    .map(((num, title, body)) => panel([
      #align(center)[
        #circle(radius: 15pt, fill: ink)[#align(center + horizon)[#text(fill: white, weight: "bold")[#num]]]
        #v(0.45in)
        #text(size: 21pt, weight: "bold")[#title]
        #v(0.2in)
        #text(size: 14.5pt, fill: muted)[#body]
      ]
    ], fill: white, height: 4.95in)))
]
#place(bottom + left, dx: margin-x, dy: -0.62in)[#text(size: 18pt, weight: "bold", fill: wine)[問題不是患者沒有說，而是重要訊號沒有被整理出來。]]
#footer(2)
#pagebreak()

// 03 — solution
#head("貳", "解決方案", "LISTEN · STRUCTURE · REVIEW", 3)
#place(left + top, dx: margin-x, dy: content-y)[
  #deck-grid(columns: (1fr, 0.34in, 1fr, 0.34in, 1fr), gutter: 0.1in,
    panel([#tag("01") #v(0.3in) #text(size: 22pt, weight: "bold")[傾聽自然對話] #v(0.18in) #text(size: 14.5pt, fill: muted)[不打斷原有醫病互動，即時將語音轉成逐字稿。]], fill: white, height: 4.45in),
    align(center + horizon)[#text(size: 30pt, fill: wine)[→]],
    panel([#tag("02") #v(0.3in) #text(size: 22pt, weight: "bold")[整理心理線索] #v(0.18in) #text(size: 14.5pt, fill: muted)[依 BSRS-5 面向整理分數草稿、原話、理由與信心。]], fill: blush, height: 4.45in),
    align(center + horizon)[#text(size: 30pt, fill: wine)[→]],
    panel([#tag("03") #v(0.3in) #text(size: 22pt, weight: "bold")[交由專業確認] #v(0.18in) #text(size: 14.5pt, fill: muted)[資訊不足就標示缺漏；由醫療人員追問、修改與確認。]], fill: white, height: 4.45in)
  )
]
#place(bottom + left, dx: margin-x, dy: -0.72in)[#box(width: content-w, fill: wine, radius: 5pt, inset: 13pt)[#align(center)[#text(size: 17pt, weight: "bold", fill: white)[用傾聽取代填表，讓每個建議都能回到患者原話。]]]]
#footer(3)
#pagebreak()

// 04 — safety
#head("參", "安全架構", "AI DRAFTS · CLINICIANS DECIDE", 4)
#place(left + top, dx: margin-x, dy: content-y)[
  #deck-grid(columns: (1fr, 1fr, 1fr, 1fr), gutter: gap,
    ..(("01", "即時轉錄", "完成轉錄後，原始音訊即時銷毀。"),
       ("02", "本機去識別", "資料離開設備前，先移除可識別資訊。"),
       ("03", "證據約束", "沒有原話支持，就輸出資訊不足。"),
       ("04", "人工決策", "追問、評分與處置皆由專業人員完成。"))
    .map(((num, title, body)) => panel([#text(size: 29pt, weight: "bold", fill: wine)[#num] #v(0.18in) #text(size: 18pt, weight: "bold")[#title] #v(0.14in) #text(size: 13.5pt, fill: muted)[#body]], fill: white, height: 2.55in)))
]
#place(left + top, dx: margin-x, dy: 4.12in)[
  #deck-grid(columns: (1fr, 1fr), gutter: gap,
    panel([#text(size: 18pt, weight: "bold", fill: wine)[系統會做] #v(0.12in) #bullet[整理已出現的心理風險線索] #v(0.08in) #bullet[保留模型版本與人工修改紀錄]], fill: blush, height: 2.08in),
    panel([#text(size: 18pt, weight: "bold")[系統不會做] #v(0.12in) #bullet[自行診斷或判定自殺意圖] #v(0.08in) #bullet[用單一分數宣告安全或危險]], fill: sand, height: 2.08in)
  )
]
#footer(4)
#pagebreak()

// 05 — demo
#head("肆", "Demo", "FROM NATURAL SPEECH TO REVIEWABLE EVIDENCE", 5)
#place(left + top, dx: margin-x, dy: content-y)[
  #deck-grid(columns: (4.0in, 0.5in, 1fr), gutter: gap,
    panel([#tag("診間自然對話") #v(0.25in) #text(size: 24pt, weight: "bold")[「最近晚上都睡不好，小孩稍微吵一下我就想罵人，覺得自己是個很糟糕的媽媽……」] #v(0.3in) #text(size: 12.5pt, fill: muted)[患者不必先理解量表，也不必離開原本的敘事脈絡。]], fill: white, height: 4.95in),
    align(center + horizon)[#text(size: 38pt, fill: wine)[→]],
    panel([
      #grid(columns: (1fr, 1fr, 1fr), gutter: 10pt,
        ..(("睡眠困難", "3", "高"), ("易怒", "3", "高"), ("自卑", "2", "中")).map(((name, score, conf)) => block(fill: cream, radius: 5pt, inset: 12pt)[#text(size: 12pt, fill: muted)[#name] #linebreak() #text(size: 28pt, weight: "bold", fill: wine)[#score] #text(size: 10pt, fill: muted, [／4 · 信心 ] + conf)]))
      #v(0.2in) #text(size: 15pt, weight: "bold")[原文證據] #v(0.08in)
      #box(width: 100%, fill: blush, radius: 5pt, inset: 13pt)[#text(size: 14pt)[「最近晚上都睡不好」 → 睡眠困難]] #v(0.11in)
      #box(width: 100%, fill: blush, radius: 5pt, inset: 13pt)[#text(size: 14pt)[「覺得自己是個很糟糕的媽媽」 → 自卑]] #v(0.18in)
      #tag("待醫療人員確認", fill: wine)
    ], fill: white, height: 4.95in)
  )
]
#place(bottom + left, dx: margin-x, dy: -0.6in)[#text(size: 17pt, weight: "bold", fill: wine)[不硬猜：證據不足就標示「資訊不足」，而不是補出一個分數。]]
#footer(5)
#pagebreak()

// 06 — market, business, competition
#head("伍", "市場、商業模式與競爭", "CUSTOMER · REVENUE · DIFFERENTIATION", 6)
#place(left + top, dx: margin-x, dy: content-y)[
  #deck-grid(columns: (1fr, 1fr, 1fr), gutter: gap,
    panel([#tag("市場切入") #v(0.22in) #text(size: 19pt, weight: "bold")[先從高需求場域開始] #v(0.16in) #bullet[精神科／身心科門診] #v(0.1in) #bullet[心理諮商與家醫科] #v(0.1in) #bullet[學校輔導中心]], fill: white, height: 4.82in),
    panel([#tag("商業模式") #v(0.22in) #text(size: 19pt, weight: "bold")[依規模與整合深度收費] #v(0.16in) #bullet[SaaS 帳號／據點／時數訂閱] #v(0.1in) #bullet[HIS、EMR API 授權] #v(0.1in) #bullet[大型院所私有部署]], fill: white, height: 4.82in),
    panel([#tag("競爭差異") #v(0.22in) #text(size: 19pt, weight: "bold")[補強現行流程，不取代它] #v(0.16in) #bullet[比純問卷更貼近自然敘事] #v(0.1in) #bullet[比人工筆記更易回溯原話] #v(0.1in) #bullet[以人工確認守住臨床界線]], fill: blush, height: 4.82in)
  )
]
#place(bottom + left, dx: margin-x, dy: -0.62in)[#text(size: 16.5pt, weight: "bold", fill: wine)[定位：可追溯的評估草稿層，介於自然對話與正式臨床判斷之間。]]
#footer(6)
#pagebreak()

// 07 — goals
#head("陸", "短長期目標", "VALIDATE FIRST · INTEGRATE NEXT", 7)
#place(left + top, dx: margin-x, dy: content-y)[
  #deck-grid(columns: (1fr, 1fr), gutter: gap,
    panel([#tag("短期｜驗證可用性") #v(0.28in) #text(size: 22pt, weight: "bold", fill: wine)[從概念 Demo 走向封閉式試辦] #v(0.2in) #bullet[完成逐字稿、證據引用與量表介面] #v(0.12in) #bullet[建立標註測試集，檢驗漏報與誤報] #v(0.12in) #bullet[邀請臨床、法規、資安與個資專家審查] #v(0.12in) #bullet[規劃倫理審查核准的封閉式試辦]], fill: white, height: 4.95in),
    panel([#tag("長期｜整合與擴展") #v(0.28in) #text(size: 22pt, weight: "bold", fill: wine)[以證據支持產品導入與宣稱] #v(0.2in) #bullet[串接 HIS／EMR 與院所權限系統] #v(0.12in) #bullet[建立版本、稽核與事件應變機制] #v(0.12in) #bullet[驗證不同語言、口音與族群偏差] #v(0.12in) #bullet[依臨床證據調整產品定位與效益宣稱]], fill: blush, height: 4.95in)
  )
]
#footer(7)
#pagebreak()

// 08 — cost
#head("柒", "成本分析", "COST DRIVERS · REVENUE LOGIC", 8)
#place(left + top, dx: margin-x, dy: content-y)[
  #deck-grid(columns: (1.25fr, 0.75fr), gutter: gap,
    panel([
      #text(size: 20pt, weight: "bold", fill: wine)[主要成本結構] #v(0.2in)
      #grid(columns: (1fr, 1fr), gutter: 12pt,
        ..(("AI 推論", "語音轉錄與 LLM 分析用量"), ("產品開發", "前端、後端與系統整合"), ("安全合規", "去識別、加密、稽核與審查"), ("維運服務", "監控、客服、模型與提示版本管理")).map(((title, body)) => block(fill: cream, radius: 5pt, inset: 13pt)[#text(size: 15pt, weight: "bold")[#title] #linebreak() #text(size: 12.5pt, fill: muted)[#body]]))
      #v(0.22in)
      #box(width: 100%, fill: blush, radius: 5pt, inset: 14pt)[#text(size: 15pt, weight: "bold", fill: wine)[單位成本公式] #linebreak() #text(size: 14pt)[每月固定成本 ＋ 單次轉錄／分析成本 × 使用量]]
    ], fill: white, height: 4.95in),
    panel([
      #tag("收入對應") #v(0.28in)
      #text(size: 20pt, weight: "bold")[讓收費結構覆蓋不同成本來源] #v(0.2in)
      #bullet[訂閱費支應產品與日常維運] #v(0.12in)
      #bullet[用量費反映 AI 推論成本] #v(0.12in)
      #bullet[整合費涵蓋 HIS／EMR 導入] #v(0.12in)
      #bullet[私有部署另計環境與稽核成本]
      #v(0.3in)
      #text(size: 13pt, fill: muted)[正式定價須在試辦後，依實際使用量、導入工時與院所採購意願驗證。]
    ], fill: sand, height: 4.95in)
  )
]
#footer(8)
#pagebreak()

// 09 — closing
#set page(fill: wine)
#place(left + top, dx: 0.68in, dy: 0.6in)[#text(size: 10pt, tracking: 2pt, fill: white)[INVISIBLE BSRS · HUMAN-IN-THE-LOOP]]
#place(left + horizon, dx: 0.72in, dy: -0.15in)[
  #text(size: 36pt, weight: "bold", fill: white)[我們不是要讓 AI 決定誰有危險，]
  #v(0.12in) #text(size: 36pt, weight: "bold", fill: white)[而是讓每一句不容易說出口的求救，]
  #v(0.12in) #text(size: 36pt, weight: "bold", fill: white)[都有機會被專業人員看見。]
]
#place(bottom + left, dx: 0.72in, dy: -0.6in)[#text(size: 14pt, fill: rgb("#E9CAC5"))[用傾聽取代填表｜AI 產生草稿｜專業人員完成判斷]]
#place(bottom + right, dx: -0.72in, dy: -0.6in)[#text(size: 12pt, fill: white)[僅供臨床參考，非醫療診斷]]
