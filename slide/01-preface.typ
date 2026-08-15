#import "theme.typ": *

#head("零", "前言", "WHY THIS MATTERS · CURRENT SCREENING", 2)

#place(left + top, dx: margin-x, dy: 1.43in)[
  #deck-grid(columns: (1fr, 1fr), gutter: 0.28in,
    panel([
      #align(center)[
        #block(width: 3.82in, height: 3.82in, radius: 9pt, clip: true)[
          #image("assets/preface-suicide-rate.png", width: 100%, height: 100%, fit: "cover")
        ]
      ]
      #v(0.14in)
      #grid(columns: (0.42in, 1fr), column-gutter: 8pt,
        box(width: 0.36in, height: 0.36in, fill: wine, radius: 50%)[
          #align(center + horizon)[#text(size: 12pt, weight: "bold", fill: white)[1]]
        ],
        block[
          #text(size: 21pt, weight: "bold")[自殺率仍在高點]
          #v(-0.13in)
          #text(size: 12.5pt, fill: muted)[當風險升高，及早辨識很重要。]
        ]
      )
    ], fill: white, height: 5.30in, inset: 14pt),

    panel([
      #align(center)[
        #block(width: 3.82in, height: 3.82in, radius: 9pt, clip: true)[
          #image("assets/preface-bsrs-scale.png", width: 100%, height: 100%, fit: "cover")
        ]
      ]
      #v(0.14in)
      #grid(columns: (0.42in, 1fr), column-gutter: 8pt,
        box(width: 0.36in, height: 0.36in, fill: wine, radius: 50%)[
          #align(center + horizon)[#text(size: 12pt, weight: "bold", fill: white)[2]]
        ],
        block[
          #text(size: 21pt, weight: "bold")[心情溫度計 BSRS-5]
          #v(-0.13in)
          #text(size: 12.5pt, fill: muted)[現行量表有效，但仍有缺點。]
        ]
      )
    ], fill: blush, height: 5.30in, inset: 14pt)
  )
]

#footer(2)
#pagebreak()
