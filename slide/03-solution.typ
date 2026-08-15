#import "theme.typ": *

#head("貳", "解決方案", "WHAT THE PRODUCT DOES", 3)

#place(left + top, dx: margin-x, dy: 1.25in)[
  #box(width: content-w, fill: blush, radius: 6pt, inset: (x: 18pt, y: 13pt))[
    #text(size: 23pt, weight: "bold", fill: wine)[隱形溫度計：把診間對話轉成可追溯的臨床輔助 Dashboard]
    #v(0.06in)
    #text(size: 13.5pt, fill: muted)[不要求患者多填一張表，也不讓 AI 下判斷；只整理對話中值得醫師或諮商師注意的訊號。]
  ]
]

#place(left + top, dx: margin-x, dy: 2.35in)[
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
      "01", [診間／諮商對話],
      text(size: 12.5pt, fill: muted)[取得同意後，在原本的醫病或諮商互動中收集語音。],
      [不改變原有談話流程],
    ),

    align(center + horizon)[#text(size: 27pt, fill: wine)[→]],

    step-card(
      "02", [AI 訊號分析],
      [#text(size: 12.5pt)[語速與停頓] #v(0.1in)
       #text(size: 12.5pt)[音量與變化] #v(0.1in)
       #text(size: 12.5pt)[談話內容與語境]],
      [整合多模態對話訊號], fill: blush,
    ),

    align(center + horizon)[#text(size: 27pt, fill: wine)[→]],

    step-card(
      "03", [臨床輔助 Dashboard],
      [#text(size: 12.2pt)[情緒與身心線索] #v(0.07in)
       #text(size: 12.2pt)[患者原話證據] #v(0.07in)
       #text(size: 12.2pt)[資訊缺漏與信心] #v(0.07in)
       #text(size: 12.2pt)[建議追問方向]],
      [每項線索皆可回看原文],
    ),

    align(center + horizon)[#text(size: 27pt, fill: wine)[→]],

    step-card(
      "04", [專業人員使用],
      text(size: 12.5pt, fill: muted)[查看訊號與原文，決定是否追問及如何進一步評估。],
      [最終判斷由專業人員完成], fill: sand,
    )
  )
]

#place(bottom + left, dx: margin-x, dy: -0.62in)[
  #text(size: 16.5pt, weight: "bold", fill: wine)[AI 不代填量表、不自行診斷；它讓對話裡的線索更容易被看見與追問。]
]
#footer(3)
#pagebreak()
