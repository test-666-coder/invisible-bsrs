#import "theme.typ": *

#head("柒", "323–380 萬，換來一年的產品與試辦能力", "COST MIX · BURN · COVERAGE", 8)

// Cost chart and legend form one centered visual group.
#place(left + top, dx: 0.62in, dy: 1.48in)[
  #image("cost-donut.svg", width: 4.48in)
]

#place(left + top, dx: 4.82in, dy: 1.72in)[
  #block(width: 2.48in)[
    #grid(columns: (0.52in, 1fr), row-gutter: 14pt,
      [#text(size: 15pt, weight: "bold", fill: wine)[70%]], [#text(size: 14pt, weight: "bold")[產品與工程]],
      [#text(size: 15pt, weight: "bold", fill: red)[15%]], [#text(size: 14pt, weight: "bold")[臨床與合規]],
      [#text(size: 15pt, weight: "bold", fill: gold)[10%]], [#text(size: 14pt, weight: "bold")[設備與雲端]],
      [#text(size: 15pt, weight: "bold", fill: muted)[5%]], [#text(size: 14pt, weight: "bold")[工具與預備]],
    )
  ]
]

// Right: two operating metrics and one explicit business conclusion.
#place(left + top, dx: 7.68in, dy: 1.48in)[
  #block(width: 4.92in, stroke: (left: 1pt + sand), inset: (left: 0.38in))[
    #text(size: 10pt, weight: "bold", tracking: 1.4pt, fill: wine)[營運尺度]
    #v(0.19in)
    #text(size: 12pt, weight: "bold", fill: muted)[平均每月支出]
    #linebreak()
    #text(size: 32pt, weight: "bold", fill: wine)[27–32 萬]
    #v(0.24in)
    #line(length: 100%, stroke: 0.9pt + sand)
    #v(0.19in)
    #text(size: 12pt, weight: "bold", fill: muted)[100 家分層收入組合]
    #linebreak()
    #text(size: 32pt, weight: "bold", fill: wine)[ARR 約 790 萬]
    #v(0.18in)
    #text(size: 14pt, weight: "bold")[收入可覆蓋核心營運，並支應後續產品擴張。]
  ]
]

#place(left + top, dx: margin-x, dy: 5.70in)[
  #block(width: content-w)[
    #text(size: 10pt, weight: "bold", tracking: 1.2pt, fill: wine)[首年成果]
    #v(0.10in)
    #block(width: 100%, height: 0.66in, fill: white, radius: 5pt, inset: 10pt)[
      #grid(columns: (1fr, auto, 1fr, auto, 1fr), column-gutter: 12pt,
        [#align(center + horizon)[#text(size: 12pt, weight: "bold")[完成產品與安全管線]]],
        [#align(center + horizon)[#text(size: 18pt, fill: gold)[→]]],
        [#align(center + horizon)[#text(size: 12pt, weight: "bold")[封閉試辦與臨床檢驗]]],
        [#align(center + horizon)[#text(size: 18pt, fill: gold)[→]]],
        [#align(center + horizon)[#text(size: 12pt, weight: "bold")[依整合量增加人力預算]]],
      )
    ]
  ]
]

#place(bottom + left, dx: margin-x, dy: -0.58in)[
  #text(size: 8.5pt, fill: muted)[金額為首年產品與試辦階段年度規劃值；詳細計算見附錄 A1。]
]
#footer(8)
#pagebreak()
