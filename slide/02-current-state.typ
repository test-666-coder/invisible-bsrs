#import "theme.typ": *

#head("壹", "現況分析與 TA 分析", "PROBLEM · SCALE · FIRST TARGET", 2)

#place(left + top, dx: margin-x, dy: content-y)[
  #deck-grid(columns: (1.52fr, 0.9fr), gutter: gap,
    panel([
      #tag("現況分析")
      \
      #text(size: 25pt, weight: "bold")[風險不是沒有出現\ 而是沒有被主動說出來]
      #v(0.04in)

      #align(center)[
      #block(width: 100%)[
      #grid(columns: (2.85in, 0.3in, 1fr), gutter: 8pt, align: left,
        block(width: 100%, fill: cream, radius: 6pt, inset: 12pt, height: 1.32in)[
          #text(size: 10.5pt, fill: muted)[量表上的回答]
          #v(-0.1in)
          #box(width: 100%, fill: white, radius: 6pt, stroke: 2pt + sand, inset: 8pt)[
            #grid(columns: (18pt, 1fr), column-gutter: 8pt, align: horizon,
              box(width: 14pt, height: 14pt, fill: wine, radius: 2pt)[
                #align(center + horizon)[#text(size: 9pt, weight: "bold", fill: white)[✓]]
              ],
              text(size: 14pt, weight: "bold")[沒有，我還好]
            )
          ]
          #v(-0.1in)
          #text(size: 10pt, fill: muted)[仰賴患者主動承認]
        ],
        align(center + horizon)[#text(size: 22pt, weight: "bold", fill: wine)[≠]],
        block(width: 100%, fill: blush, radius: 6pt, inset: 12pt, height: 1.32in)[
          #text(size: 10.5pt, fill: wine)[自然對話中的線索]
          #v(-0.1in)
          #text(size: 20pt, weight: "bold", fill: wine)[「X你XXX，我沒有易怒」]
          #v(-0.1in)
          #text(size: 10pt, fill: muted)[症狀已經出現在敘事裡]
        ]
      )
      ]
      ]

      #v(0in)
      #line(length: 100%, stroke: 0.8pt + sand)
      #v(0in)

      #grid(columns: (1.05fr, 1.35fr), gutter: 15pt,
        block[
          #text(size: 10.5pt, weight: "bold", fill: wine)[問題規模｜114 年台灣]
          #v(0.05in)
          #text(size: 32pt, weight: "bold", fill: wine)[3,951]
          #text(size: 10.5pt, fill: muted)[ 人死於自殺]
        ],
        block[
          #text(size: 15pt, weight: "bold")[不能只等患者主動求助]
          #v(0.09in)
          #text(size: 12pt)[每十萬人口 16.9 人　｜　平均每天約 11 人]
        ]
      )
    ], fill: white, height: 4.95in),

    panel([
      #tag("第一階段 TA")
      #v(0.18in)
      #text(size: 19pt, weight: "bold", fill: wine)[身心科診所]
      #text(size: 19pt, weight: "bold", fill: wine)[心理諮商機構]
      #v(0.22in)

      #text(size: 10.5pt, weight: "bold", fill: wine)[01｜誰買單]
      #v(0.04in)
      #text(size: 13.5pt, weight: "bold")[診所與諮商機構]
      #v(0.16in)

      #text(size: 10.5pt, weight: "bold", fill: wine)[02｜誰使用]
      #v(0.04in)
      #text(size: 13.5pt, weight: "bold")[醫師、心理師、諮商師]
      #v(0.16in)

      #text(size: 10.5pt, weight: "bold", fill: wine)[03｜要完成什麼工作]
      #v(0.04in)
      #text(size: 13.5pt, weight: "bold")[在有限時間內掌握]
      #v(0.06in)
      #text(size: 12.5pt)[線索　原文　待追問項目]
    ], fill: sand, height: 4.95in)
  )
]

#place(bottom + left, dx: margin-x, dy: -0.34in)[
]
#place(bottom + right, dx: -margin-x, dy: -0.14in)[
  #text(size: 8pt, fill: muted)[資料：衛福部「114 年國人死因統計結果」]
]
#footer(2)
#pagebreak()
