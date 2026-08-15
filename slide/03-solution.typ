#import "theme.typ": *

#head("貳", "解決方案", "WHAT THE PRODUCT DOES", 3)

#place(left + top, dx: margin-x, dy: 1.25in)[
  #box(width: content-w, fill: blush, radius: 6pt, inset: (x: 18pt, y: 13pt))[
    #text(size: 23pt, weight: "bold", fill: wine)[隱形溫度計：把診間對話轉成可追溯的臨床輔助 Dashboard]
    #v(0.06in)
    #text(size: 13.5pt, fill: muted)[從語音、隱私處理到結構化輸出，將自然對話整理成供專業人員覆核的評估草稿。]
  ]
]

#place(left + top, dx: margin-x, dy: 2.72in)[
  #let step-card(no, title, body, foot, fill: white) = panel([
    #grid(
      rows: (0.38in, 0.72in, 1.35in, 0.48in),
      row-gutter: 0.08in,
      tag(no),
      align(left + horizon)[#text(size: 16pt, weight: "bold")[#title]],
      align(left + top)[#body],
      align(left + horizon)[
        #box(width: 100%, fill: cream, radius: 4pt, inset: (x: 8pt, y: 7pt))[
          #align(center)[#text(size: 10.5pt, weight: "bold", fill: wine)[#foot]]
        ]
      ],
    )
  ], fill: fill, height: 3.42in, inset: 16pt)

  #deck-grid(columns: (1fr, 0.24in, 1fr, 0.24in, 1fr, 0.24in, 1fr), gutter: 0.07in,
    step-card(
      "01", [語音與逐字稿],
      [#text(size: 12.5pt)[本地 Whisper 轉錄] #v(0.1in)
       #text(size: 12.5pt)[同步取得語音情緒]],
      [輸入來自自然醫病對話],
    ),

    align(center + horizon)[#text(size: 27pt, fill: wine)[→]],

    step-card(
      "02", [本機隱私處理],
      [#text(size: 12.5pt)[CKIP NER 辨識個資] #v(0.1in)
       #text(size: 12.5pt)[Regex 補強遮蔽] #v(0.1in)
       #text(size: 12.5pt)[只送出去識別文字]],
      [原始音訊不進入 LLM], fill: blush,
    ),

    align(center + horizon)[#text(size: 27pt, fill: wine)[→]],

    step-card(
      "03", [結構化 AI 分析],
      [#text(size: 12.2pt)[BSRS-5 五項線索] #v(0.07in)
       #text(size: 12.2pt)[自殺想法獨立處理] #v(0.07in)
       #text(size: 12.2pt)[證據、信心與缺漏] #v(0.07in)
       #text(size: 12.2pt)[固定 Schema 驗證]],
      [資訊不足就要求直接確認],
    ),

    align(center + horizon)[#text(size: 27pt, fill: wine)[→]],

    step-card(
      "04", [Dashboard 覆核],
      [#text(size: 12.5pt)[查看分項與原話] #v(0.1in)
       #text(size: 12.5pt)[確認、修改或追問] #v(0.1in)
       #text(size: 12.5pt)[匯出結構化 JSON]],
      [正式判斷由專業人員完成], fill: sand,
    )
  )
]

#place(bottom + left, dx: margin-x, dy: -0.62in)[
  #text(size: 16.5pt, weight: "bold", fill: wine)[AI 不代填量表、不自行診斷；它讓對話裡的線索更容易被看見與追問。]
]
#footer(3)
#pagebreak()
