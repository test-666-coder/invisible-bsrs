#import "theme.typ": *

#head("附錄", "成本明細｜一年如何算到 380 萬", "A1 · ANNUAL COST BUILD-UP", "A1")

#place(left + top, dx: margin-x, dy: 1.45in)[
  #block(width: content-w)[
    #grid(columns: (2.5fr, 0.72fr, 0.72fr, 1.2fr), column-gutter: 14pt, row-gutter: 11pt,
      [#text(size: 11pt, weight: "bold", fill: muted)[成本項目]],
      [#align(right)[#text(size: 11pt, weight: "bold", fill: muted)[低估]]],
      [#align(right)[#text(size: 11pt, weight: "bold", fill: muted)[高估]]],
      [#align(right)[#text(size: 11pt, weight: "bold", fill: muted)[計算基準]]],

      [#text(size: 13pt, weight: "bold")[核心產品與工程基本薪資]], [#align(right)[234]], [#align(right)[234]], [#align(right)[19.5 萬／月]],
      [#text(size: 13pt)[雇主負擔與獎金緩衝]], [#align(right)[35]], [#align(right)[50]], [#align(right)[薪資 15–21%]],
      [#text(size: 13pt)[臨床顧問與案例標註]], [#align(right)[24]], [#align(right)[36]], [#align(right)[2–3 萬／月]],
      [#text(size: 13pt)[資安、法規與法律諮詢]], [#align(right)[15]], [#align(right)[25]], [#align(right)[專案支出]],
      [#text(size: 13pt)[設備、雲端與測試環境]], [#align(right)[10]], [#align(right)[20]], [#align(right)[依用量]],
      [#text(size: 13pt)[工具、維運與預備金]], [#align(right)[5]], [#align(right)[15]], [#align(right)[風險緩衝]],
    )
    #v(0.25in)
    #line(length: 100%, stroke: 1.2pt + sand)
    #v(0.18in)
    #grid(columns: (2.5fr, 0.72fr, 0.72fr, 1.2fr), column-gutter: 14pt,
      [#text(size: 18pt, weight: "bold", fill: wine)[年度合計]],
      [#align(right)[#text(size: 22pt, weight: "bold", fill: wine)[323]]],
      [#align(right)[#text(size: 22pt, weight: "bold", fill: wine)[380]]],
      [#align(right)[#text(size: 11pt, weight: "bold")[新台幣萬元]]],
    )
    #v(0.28in)
    #grid(columns: (1fr, 1fr), column-gutter: 0.28in,
      box(fill: blush, radius: 5pt, inset: 13pt)[
        #text(size: 11pt, weight: "bold", fill: wine)[人力與專業服務]
        #linebreak()
        #text(size: 19pt, weight: "bold")[308–345 萬]
      ],
      box(fill: sand, radius: 5pt, inset: 13pt)[
        #text(size: 11pt, weight: "bold", fill: wine)[技術、工具與緩衝]
        #linebreak()
        #text(size: 19pt, weight: "bold")[15–35 萬]
      ],
    )
    #v(0.2in)
    #text(size: 10.5pt, fill: muted)[不含創辦人薪資、辦公室、行銷、銷售與正式臨床試驗。]
  ]
]

#place(bottom + left, dx: margin-x, dy: -0.24in)[
  #text(size: 8.5pt, fill: muted)[薪資參考：104 薪資情報；其他項目依 MVP 開發、臨床與合規需求估算。]
]
#footer("A1")
#pagebreak()
#include "11-appendix-landing.typ"
