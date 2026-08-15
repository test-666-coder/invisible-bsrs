#import "theme.typ": *

#head("柒", "首年控制在 380 萬內", "COST MIX · BURN · COVERAGE", 8)

#place(left + top, dx: 0.72in, dy: 1.48in)[
  #image("cost-donut.svg", width: 4.62in)
]

#place(left + top, dx: 5.62in, dy: 1.72in)[
  #block(width: 2.20in)[
    #text(size: 13pt, weight: "bold", fill: wine)[70%]
    #text(size: 13pt, weight: "bold")[ 產品與工程]
    #v(0.16in)
    #text(size: 13pt, weight: "bold", fill: red)[15%]
    #text(size: 13pt, weight: "bold")[ 臨床與合規]
    #v(0.16in)
    #text(size: 13pt, weight: "bold", fill: gold)[10%]
    #text(size: 13pt, weight: "bold")[ 設備與雲端]
    #v(0.16in)
    #text(size: 13pt, weight: "bold", fill: muted)[5%]
    #text(size: 13pt, weight: "bold")[ 工具與預備]
  ]
]

#place(left + top, dx: 8.50in, dy: 1.65in)[
  #block(width: 4.12in, stroke: (left: 1pt + sand), inset: (left: 0.36in))[
    #tag("營運尺度") #v(0.25in)
    #text(size: 12pt, weight: "bold", fill: muted)[平均每月支出]
    #linebreak()
    #text(size: 30pt, weight: "bold", fill: wine)[27–32 萬]
    #v(0.22in)
    #text(size: 12pt, weight: "bold", fill: muted)[100 家分層收入組合]
    #linebreak()
    #text(size: 30pt, weight: "bold", fill: wine)[ARR 約 790 萬]
    #v(0.22in)
    #line(length: 100%, stroke: 1pt + sand)
    #v(0.14in)
    #text(size: 14pt, weight: "bold")[收入可覆蓋核心營運，]
    #linebreak()
    #text(size: 14pt, weight: "bold")[並支應後續產品擴張。]
  ]
]

#place(left + top, dx: margin-x, dy: 5.95in)[
  #block(width: content-w, height: 0.72in, fill: white, radius: 5pt, inset: 11pt)[
    #grid(columns: (auto, 1fr, auto, 1fr, auto, 1fr), column-gutter: 10pt,
      [#text(size: 11pt, weight: "bold", fill: wine)[MVP]], [#text(size: 10.5pt)[完成產品與安全管線]],
      [#text(size: 18pt, fill: sand)[→]], [#text(size: 10.5pt)[封閉試辦與臨床檢驗]],
      [#text(size: 18pt, fill: sand)[→]], [#text(size: 10.5pt)[依整合量增加人力預算]],
    )
  ]
]

#place(bottom + left, dx: margin-x, dy: -0.58in)[
  #text(size: 8.5pt, fill: muted)[金額為 MVP 階段年度規劃值；詳細計算見附錄 A1。]
]
#footer(8)
#pagebreak()
