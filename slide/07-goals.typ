#import "theme.typ": *

#head("陸", "短中長期目標", "VALIDATE LOCALLY · SCALE RESPONSIBLY", 7)
#place(left + top, dx: margin-x, dy: 1.34in)[
  #block(width: content-w, height: 3.05in, radius: 10pt, clip: true)[
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
        [#text(size: 15.5pt, weight: "bold")[短期｜限定範圍] #v(0.07in) #text(size: 12.5pt, fill: muted)[完成原型並於台大心輔中心試辦；以專家測試集驗證風險線索辨識。]]
      )
    ],
    block[
      #line(length: 100%, stroke: 2pt + wine)
      #v(0.12in)
      #grid(columns: (0.43in, 1fr), column-gutter: 0.12in,
        text(size: 21pt, weight: "bold", fill: wine)[02],
        [#text(size: 15.5pt, weight: "bold")[中期｜心理師共建 RAG] #v(0.07in) #text(size: 12.5pt, fill: muted)[由心理師制定準則並審核知識庫；串接台灣指引，微調專業輸出格式。]]
      )
    ],
    block[
      #line(length: 100%, stroke: 2pt + wine)
      #v(0.12in)
      #grid(columns: (0.43in, 1fr), column-gutter: 0.12in,
        text(size: 21pt, weight: "bold", fill: wine)[03],
        [#text(size: 15.5pt, weight: "bold")[長期｜國際在地化] #v(0.07in) #text(size: 12.5pt, fill: muted)[以共用核心建立各國版本；整合當地語言、文化、法規與轉介資源。]]
      )
    ]
  )
]
#footer(7)
#pagebreak()
