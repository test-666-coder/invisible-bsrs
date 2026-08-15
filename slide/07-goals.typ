#import "theme.typ": *

#head("伍", "短中長期目標", "VALIDATE LOCALLY · SCALE RESPONSIBLY", 6)

#place(left + top, dx: margin-x, dy: 1.34in)[
  #block(width: content-w, height: 3.05in, radius: 10pt, clip: true)[
    #v(0.5in)
    #image("assets/goals-roadmap.png", width: 100%, height: 100%, fit: "cover")
  ]
]
#place(left + top, dx: margin-x, dy: 4.67in)[
  #deck-grid(columns: (1fr, 1fr, 1fr), gutter: 0.34in,
    block[
      #line(length: 100%, stroke: 2pt + wine)
      #v(0.12in)
      #grid(columns: (0.43in, 1fr), column-gutter: 0.12in,
        text(size: 21pt, weight: "bold", fill: wine)[01],
        [#text(size: 15.5pt, weight: "bold")[短期｜離線驗證與試辦] #v(0.07in) #text(size: 12.5pt, fill: muted)[先以專家測試集建立離線基準；再以臺大心輔中心為首選場域，爭取封閉試辦。]]
      )
    ],
    block[
      #line(length: 100%, stroke: 2pt + wine)
      #v(0.12in)
      #grid(columns: (0.43in, 1fr), column-gutter: 0.12in,
        text(size: 21pt, weight: "bold", fill: wine)[02],
        [#text(size: 15.5pt, weight: "bold")[中期｜專家共建與付費驗證] #v(0.07in) #text(size: 12.5pt, fill: muted)[由心理師制定準則並共建 RAG；以付費試辦驗證節省時間、採納率與續約。]]
      )
    ],
    block[
      #line(length: 100%, stroke: 2pt + wine)
      #v(0.12in)
      #grid(columns: (0.43in, 1fr), column-gutter: 0.12in,
        text(size: 21pt, weight: "bold", fill: wine)[03],
        [#text(size: 15.5pt, weight: "bold")[長期｜可複製後國際化] #v(0.07in) #text(size: 12.5pt, fill: muted)[先在台灣證明續約與導入可複製；再由當地專家依文化、法規與測試集逐國驗證。]]
      )
    ]
  )
]
#footer(6)
#pagebreak()
