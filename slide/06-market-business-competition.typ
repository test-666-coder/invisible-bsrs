#import "theme.typ": *

#head("伍", "840 家切入，100 家可達 ARR 790 萬", "MARKET · PRICING · EXPANSION", 6)

// Left: one dominant market visual with its own protected caption zone.
#place(left + top, dx: 0.75in, dy: 1.45in)[
  #image("market-rings.svg", width: 5.15in)
]

#place(left + top, dx: 0.67in, dy: 5.86in)[
  #block(width: 5.15in)[
    #align(center)[
      #text(size: 10pt, weight: "bold", tracking: 1.1pt, fill: wine)[擴張順序]
      #v(0.08in)
      #text(size: 14pt, weight: "bold")[心理專科]
      #h(8pt) #text(size: 16pt, fill: gold)[→] #h(8pt)
      #text(size: 14pt, weight: "bold")[基層醫療]
      #h(8pt) #text(size: 16pt, fill: gold)[→] #h(8pt)
      #text(size: 14pt, weight: "bold")[校園]
    ]
  ]
]

// Right: a pricing ladder rather than a stack of unrelated cards.
#place(left + top, dx: 6.35in, dy: 1.50in)[
  #block(width: 6.40in)[
    #text(size: 10pt, weight: "bold", tracking: 1.4pt, fill: wine)[分層定價]
    #v(0.10in)
    #text(size: 20pt, weight: "bold")[同一套引擎，依導入深度收費]
    #v(0.19in)

    #grid(
      columns: (0.82in, 1.80in, 1fr),
      column-gutter: 14pt,
      row-gutter: 9pt,
      [#align(left + horizon)[#text(size: 14pt, weight: "bold", fill: wine)[診所]]],
      [#align(left + horizon)[#text(size: 20pt, weight: "bold")[NT\$4,800] #text(size: 11pt, fill: muted)[／月]]],
      [#align(left + horizon)[#text(size: 12pt, fill: muted)[單一據點｜低門檻導入]]],
      [#line(length: 100%, stroke: 0.8pt + sand)], [#line(length: 100%, stroke: 0.8pt + sand)], [#line(length: 100%, stroke: 0.8pt + sand)],

      [#align(left + horizon)[#text(size: 14pt, weight: "bold", fill: wine)[校園]]],
      [#align(left + horizon)[#text(size: 20pt, weight: "bold")[NT\$12 萬] #text(size: 11pt, fill: muted)[／年]]],
      [#align(left + horizon)[#text(size: 12pt, fill: muted)[多人協作｜權限與稽核]]],
      [#line(length: 100%, stroke: 0.8pt + sand)], [#line(length: 100%, stroke: 0.8pt + sand)], [#line(length: 100%, stroke: 0.8pt + sand)],

      [#align(left + horizon)[#text(size: 14pt, weight: "bold", fill: wine)[醫院]]],
      [#align(left + horizon)[#text(size: 20pt, weight: "bold")[NT\$30 萬+] #text(size: 11pt, fill: muted)[／年]]],
      [#align(left + horizon)[#text(size: 12pt, fill: muted)[系統整合｜私有化選配]]],
    )

    #v(0.24in)
    #block(width: 100%, fill: blush, radius: 6pt, inset: (x: 15pt, y: 13pt))[
      #grid(columns: (1.45fr, 1fr), column-gutter: 16pt,
        [#align(left + horizon)[
          #text(size: 10.5pt, weight: "bold", fill: muted)[100 家示範收入組合]
          #linebreak()
          #text(size: 14pt, weight: "bold")[80 診所＋15 校園＋5 醫院]
        ]],
        [#align(right + horizon)[
          #text(size: 10.5pt, weight: "bold", fill: muted)[年經常性收入]
          #linebreak()
          #text(size: 29pt, weight: "bold", fill: wine)[約 790 萬]
        ]],
      )
    ]

    #v(0.18in)
    #grid(columns: (0.18in, 1fr), column-gutter: 10pt,
      [#align(center + horizon)[#line(length: 0.18in, stroke: 2.2pt + gold)]],
      [#text(size: 12pt)[AI 醫療書記整理病歷；Invisible BSRS 補上心理風險的原話證據與待追問。]],
    )
  ]
]

#place(bottom + left, dx: margin-x, dy: -0.58in)[
  #text(size: 8.4pt, fill: muted)[SOM：840 家心理專科場域｜SAM：12,922 家醫療院所＋425 家心理機構｜TAM：再納入高中職與大專輔導體系。圈層為範圍示意；定價為本案建議方案。]
]
#footer(6)
#pagebreak()
