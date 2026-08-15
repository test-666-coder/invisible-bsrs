#import "theme.typ": *

#head("伍", "市場與商業模式：先專科，再擴張", "MARKET · PRICING · EXPANSION", 6)

// The chart and the pricing column have separate safety zones.  The wider
// gutter keeps labels in the illustration from visually touching body copy.
#place(left + top, dx: 0.62in, dy: 1.36in)[
  #image("market-rings.svg", width: 5.86in)
]

#place(left + top, dx: 7.16in, dy: 1.45in)[
  #block(width: 5.48in)[
    #tag("分層定價")
    #v(0.17in)
    #text(size: 22pt, weight: "bold", fill: ink)[同一套引擎，依導入深度收費]
    #v(0.23in)

    #grid(
      columns: (0.72in, 1.55in, 1fr),
      column-gutter: 12pt,
      row-gutter: 8pt,
      [#text(size: 12pt, weight: "bold", fill: wine)[診所]],
      [#text(size: 17pt, weight: "bold")[NT\$4,800] #text(size: 9pt, fill: muted)[／月]],
      [#text(size: 10pt, fill: muted)[單一據點｜低門檻導入]],
      [#line(length: 100%, stroke: 0.7pt + sand)],
      [#line(length: 100%, stroke: 0.7pt + sand)],
      [#line(length: 100%, stroke: 0.7pt + sand)],
      [#text(size: 12pt, weight: "bold", fill: wine)[校園]],
      [#text(size: 17pt, weight: "bold")[NT\$12 萬] #text(size: 9pt, fill: muted)[／年]],
      [#text(size: 10pt, fill: muted)[多人協作｜權限與稽核]],
      [#line(length: 100%, stroke: 0.7pt + sand)],
      [#line(length: 100%, stroke: 0.7pt + sand)],
      [#line(length: 100%, stroke: 0.7pt + sand)],
      [#text(size: 12pt, weight: "bold", fill: wine)[醫院]],
      [#text(size: 17pt, weight: "bold")[NT\$30 萬+] #text(size: 9pt, fill: muted)[／年]],
      [#text(size: 10pt, fill: muted)[系統整合｜私有化選配]],
    )

    #v(0.24in)
    #block(width: 100%, fill: blush, radius: 6pt, inset: (x: 14pt, y: 11pt))[
      #grid(columns: (1.48fr, 1fr), column-gutter: 12pt,
        [#text(size: 9.5pt, weight: "bold", fill: muted)[100 家示範收入組合]
         #linebreak()
         #text(size: 12pt, weight: "bold")[80 診所＋15 校園＋5 醫院]],
        [#align(right)[
          #text(size: 9.5pt, weight: "bold", fill: muted)[年經常性收入]
          #linebreak()
          #text(size: 24pt, weight: "bold", fill: wine)[約 790 萬]
        ]],
      )
    ]
    #v(0.16in)
    #grid(columns: (0.12in, 1fr), column-gutter: 9pt,
      [#line(length: 0.12in, stroke: 2pt + gold)],
      [#text(size: 10pt)[AI 醫療書記整理病歷；Invisible BSRS 補上心理風險的原話證據與待追問。]],
    )
  ]
]

#place(bottom + left, dx: margin-x, dy: -0.58in)[
  #text(size: 8.2pt, fill: muted)[SOM：840 家心理專科場域｜SAM：12,922 家醫療院所＋425 家心理機構｜TAM：再納入高中職與大專輔導體系。圈層為範圍示意；定價為本案建議方案。]
]
#footer(6)
#pagebreak()
