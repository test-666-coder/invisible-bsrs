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
  place(top + left, dx: 0.46in, dy: 0.36in)[
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

// 02 — problem
#head("壹", "現況分析", "THE SIGNALS ARE ALREADY IN THE CONVERSATION", 2)
#place(left + top, dx: margin-x, dy: content-y)[
  #deck-grid(columns: (1fr, 1fr, 1fr), gutter: gap,
    ..(
      ("1", "低報風險", "防衛、污名或缺乏信任，讓真正的困擾不一定出現在量表上。"),
      ("2", "時間有限", "醫療人員同時要建立關係、理解主訴，也要辨識心理風險。"),
      ("3", "線索分散", "失眠、易怒、自我否定常藏在自然敘述裡，容易被匆忙略過。"),
    ).map(((num, title, body)) => panel([
      #align(center)[
        #circle(radius: 15pt, fill: ink)[#align(center + horizon)[#text(fill: white, weight: "bold")[#num]]]
        #v(0.18in)
        #text(size: 21pt, weight: "bold")[#title]
        #v(0.14in)
        #text(size: 14.5pt, fill: muted)[#body]
      ]
      #place(bottom + center, dy: -0.15in)[#box(width: 100%, fill: wine, radius: 6pt, inset: 10pt)[
        #align(center)[#text(fill: white, size: 13pt, weight: "bold")[需要更自然、可追溯的輔助方式]]
      ]]
    ], fill: white, height: 4.95in))
  )
]
#place(bottom + left, dx: margin-x, dy: -0.62in)[
  #text(size: 18pt, weight: "bold", fill: wine)[問題不是患者沒有說，而是重要訊號沒有被整理出來。]
]
#footer(2)
#pagebreak()

// 03 — demo
#head("貳", "系統展示", "FROM NATURAL SPEECH TO REVIEWABLE EVIDENCE", 3)
#place(left + top, dx: margin-x, dy: content-y)[
  #deck-grid(columns: (4.0in, 0.5in, 1fr), gutter: gap,
    panel([
      #tag("診間自然對話")
      #v(0.25in)
      #text(size: 24pt, weight: "bold", fill: ink)[「最近晚上都睡不好，小孩稍微吵一下我就想罵人，覺得自己是個很糟糕的媽媽……」]
      #v(0.32in)
      #text(size: 12pt, fill: muted)[患者不必先理解量表，也不必離開原本的敘事脈絡。]
    ], fill: white, height: 4.95in),
    align(center + horizon)[#text(size: 38pt, fill: wine)[→]],
    panel([
      #grid(columns: (1fr, 1fr, 1fr), gutter: 10pt,
        ..(("睡眠困難", "3", "高"), ("易怒", "3", "高"), ("自卑", "2", "中"))
          .map(((name, score, conf)) => block(fill: cream, radius: 5pt, inset: 12pt)[
        #text(size: 12pt, fill: muted)[#name]
        #linebreak()
        #text(size: 28pt, weight: "bold", fill: wine)[#score]
        #text(size: 10pt, fill: muted, [／4 · 信心 ] + conf)
      ]))
      #v(0.2in)
      #text(size: 15pt, weight: "bold")[原文證據]
      #v(0.08in)
      #box(width: 100%, fill: blush, radius: 5pt, inset: 13pt)[
        #text(size: 14pt)[「最近晚上都睡不好」 → 睡眠困難]
      ]
      #v(0.11in)
      #box(width: 100%, fill: blush, radius: 5pt, inset: 13pt)[
        #text(size: 14pt)[「覺得自己是個很糟糕的媽媽」 → 自卑]
      ]
      #v(0.18in)
      #tag("待醫療人員確認", fill: wine)
    ], fill: white, height: 4.95in)
  )
]
#place(bottom + left, dx: margin-x, dy: -0.6in)[
  #text(size: 17pt, weight: "bold", fill: wine)[不硬猜：證據不足就標示「資訊不足」，而不是補出一個分數。]
]
#footer(3)
#pagebreak()

// 04 — workflow and safety
#head("參", "安全架構", "AI DRAFTS · CLINICIANS DECIDE", 4)
#place(left + top, dx: margin-x, dy: content-y)[
  #deck-grid(columns: (1fr, 1fr, 1fr, 1fr), gutter: gap,
    ..(("01", "即時轉錄", "診間語音轉為逐字稿；完成後銷毀原始音訊。"),
    ("02", "本機去識別", "資料離開設備前，先移除姓名、電話、地址。"),
    ("03", "結構化分析", "輸出分數草稿、原話、理由、信心與缺漏。"),
    ("04", "人工確認", "醫療人員追問、修改後，才依院所流程記錄。"))
    .map(((num, title, body)) => panel([
    #text(size: 29pt, weight: "bold", fill: wine)[#num]
    #v(0.13in)
    #text(size: 18pt, weight: "bold")[#title]
    #v(0.14in)
    #text(size: 13.5pt, fill: muted)[#body]
  ], fill: white, height: 2.6in)))
]
#place(left + top, dx: margin-x, dy: 4.18in)[
  #deck-grid(columns: (1fr, 1fr), gutter: gap,
    panel([
      #text(size: 17pt, weight: "bold", fill: wine)[系統會做]
      #v(0.12in)
      #bullet[整理已出現的心理風險線索]
      #v(0.08in)
      #bullet[讓每個建議都能回到患者原話]
    ], fill: blush, height: 2.05in),
    panel([
      #text(size: 17pt, weight: "bold", fill: ink)[系統不會做]
      #v(0.12in)
      #bullet[自行診斷憂鬱症或判定自殺意圖]
      #v(0.08in)
      #bullet[用單一模型分數宣告安全或危險]
    ], fill: sand, height: 2.05in)
  )
]
#footer(4)
#pagebreak()

// 05 — business
#head("肆", "商業模式", "WHO PAYS · WHAT THEY GET · HOW WE SCALE", 5)
#place(left + top, dx: margin-x, dy: content-y)[
  #deck-grid(columns: (1fr, 1fr, 1fr), gutter: gap,
    panel([
      #tag("目標客群")
      #v(0.2in)
      #text(size: 19pt, weight: "bold")[先從高需求場域切入]
      #v(0.16in)
      #bullet[精神科／身心科門診]
      #v(0.1in)
      #bullet[心理諮商與家醫科]
      #v(0.1in)
      #bullet[學校輔導中心]
    ], fill: white, height: 4.8in),
    panel([
      #tag("價值主張")
      #v(0.2in)
      #text(size: 19pt, weight: "bold")[讓傾聽更完整，不增加填表負擔]
      #v(0.16in)
      #bullet[縮短整理量表草稿時間]
      #v(0.1in)
      #bullet[提醒容易忽略的線索]
      #v(0.1in)
      #bullet[原話可追溯、便於複核]
    ], fill: white, height: 4.8in),
    panel([
      #tag("收益模式")
      #v(0.2in)
      #text(size: 19pt, weight: "bold")[依院所規模與整合深度收費]
      #v(0.16in)
      #bullet[SaaS 帳號／據點／時數訂閱]
      #v(0.1in)
      #bullet[HIS、EMR API 模組授權]
      #v(0.1in)
      #bullet[大型院所私有部署]
    ], fill: white, height: 4.8in)
  )
]
#place(bottom + left, dx: margin-x, dy: -0.66in)[
  #box(width: content-w, fill: blush, radius: 5pt, inset: 14pt)[
    #text(size: 16pt, weight: "bold", fill: wine)[進入策略：] #text(size: 15pt)[以封閉式試辦驗證臨床工作流，再透過醫療資訊系統合作擴大導入。]
  ]
]
#footer(5)
#pagebreak()

// 06 — roadmap
#head("伍", "成效與規劃", "FROM CONCEPT DEMO TO CLINICAL PILOT", 6)
#place(left + top, dx: margin-x, dy: content-y)[
  #deck-grid(columns: (1fr, 1fr, 1fr, 1fr), gutter: gap,
    ..(("實作", "概念驗證", ("固定模擬逐字稿", "定義輸出 schema", "完成量表與證據介面")),
    ("短期", "離線驗證", ("建立標註測試集", "測試漏報、誤報與語境", "完成 PII 與刪除流程")),
    ("中期", "封閉式試辦", ("臨床／法規／資安審查", "取得倫理審查核准", "觀察可用性與工作流")),
    ("長期", "系統整合", ("串接 HIS／EMR", "權限、稽核與版本紀錄", "依證據調整產品宣稱")))
    .map(((stage, title, items)) => panel([
    #align(center)[#tag(stage)]
    #v(0.18in)
    #align(center)[#text(size: 19pt, weight: "bold", fill: wine)[#title]]
    #v(0.2in)
    #for item in items [
      #bullet[#item]
      #v(0.14in)
    ]
  ], fill: white, height: 4.85in)))
]
#place(bottom + left, dx: margin-x, dy: -0.64in)[
  #text(size: 17pt, weight: "bold", fill: wine)[成功不是 AI 打了幾分，而是醫療人員能否更快找到值得追問的證據。]
]
#footer(6)
#pagebreak()

// 07 — closing
#set page(fill: wine)
#place(left + top, dx: 0.68in, dy: 0.6in)[
  #text(size: 10pt, tracking: 2pt, fill: white)[INVISIBLE BSRS · HUMAN-IN-THE-LOOP]
]
#place(left + horizon, dx: 0.72in, dy: -0.15in)[
  #text(size: 36pt, weight: "bold", fill: white)[我們不是要讓 AI 決定誰有危險，]
  #v(0.12in)
  #text(size: 36pt, weight: "bold", fill: white)[而是讓每一句不容易說出口的求救，]
  #v(0.12in)
  #text(size: 36pt, weight: "bold", fill: white)[都有機會被專業人員看見。]
]
#place(bottom + left, dx: 0.72in, dy: -0.6in)[
  #text(size: 14pt, fill: rgb("#E9CAC5"))[用傾聽取代填表｜AI 產生草稿｜專業人員完成判斷]
]
#place(bottom + right, dx: -0.72in, dy: -0.6in)[
  #text(size: 12pt, fill: white)[僅供臨床參考，非醫療診斷]
]
