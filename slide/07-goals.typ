#import "theme.typ": *

#head("陸", "先在封閉場域驗證，再決定擴張", "OFFLINE TEST · CAMPUS PILOT · SCALE", 7)

#place(left + top, dx: 0.72in, dy: 1.38in)[
  #block(width: 11.9in)[
    #text(size: 16pt, weight: "bold")[試辦場域要能看見真實工作流，也要把風險關在可控範圍內。]
    #v(0.1in)
    #text(size: 10.5pt, fill: muted)[因此先做離線基準，再優先接洽臺大學務處學生心理輔導中心；取得必要同意與審查後，才進入封閉試辦。]
  ]
]

// One continuous route replaces the previous pair of dense cards.
#place(left + top, dx: 2.37in, dy: 2.38in)[
  #line(length: 8.18in, stroke: 2pt + sand)
]
#place(left + top, dx: 2.245in, dy: 2.27in)[#circle(radius: 9pt, fill: cream, stroke: 2pt + wine)]
#place(left + top, dx: 6.279in, dy: 2.21in)[#circle(radius: 13pt, fill: wine, stroke: 3pt + blush)]
#place(left + top, dx: 10.425in, dy: 2.27in)[#circle(radius: 9pt, fill: cream, stroke: 2pt + wine)]

#place(left + top, dx: 0.72in, dy: 2.72in)[
  #grid(columns: (3.30in, 3.94in, 3.30in), column-gutter: 0.47in,
    block[
      #text(size: 10pt, weight: "bold", fill: wine)[01　離線基準]
      #v(0.12in)
      #text(size: 19pt, weight: "bold")[先證明系統不亂報]
      #v(0.18in)
      #text(size: 11pt, fill: muted)[合成與去識別逐字稿]
      #linebreak()
      #text(size: 11pt, fill: muted)[標註 BSRS、原話證據與待追問]
      #v(0.19in)
      #text(size: 10pt, weight: "bold")[通過門檻]
      #linebreak()
      #text(size: 10pt)[漏失率、證據定位與誤報可量化]
    ],
    block(fill: blush, radius: 7pt, inset: 15pt)[
      #text(size: 10pt, weight: "bold", fill: wine)[02　首選試辦場域]
      #v(0.10in)
      #text(size: 20pt, weight: "bold", fill: wine)[優先接洽臺大心輔中心]
      #v(0.15in)
      #text(size: 10.5pt)[初談、諮商與轉介流程完整，適合觀察跨專業協作中的真實使用情境。]
      #v(0.17in)
      #text(size: 9.5pt, weight: "bold")[進場前置]
      #linebreak()
      #text(size: 9.5pt)[校方與知情同意｜去識別化｜個資、資安及必要倫理審查]
    ],
    block[
      #text(size: 10pt, weight: "bold", fill: wine)[03　商業化擴張]
      #v(0.12in)
      #text(size: 19pt, weight: "bold")[試辦成功才接正式流程]
      #v(0.18in)
      #text(size: 11pt, fill: muted)[先切入 840 家心理專科場域]
      #linebreak()
      #text(size: 11pt, fill: muted)[再整合基層醫療與更多校園]
      #v(0.19in)
      #text(size: 10pt, weight: "bold")[擴張門檻]
      #linebreak()
      #text(size: 10pt)[專業人員接受度、修改時間與風險事件]
    ],
  )
]

#place(left + top, dx: 0.72in, dy: 5.72in)[
  #block(width: 11.9in, fill: white, radius: 5pt, inset: (x: 14pt, y: 10pt))[
    #grid(columns: (1.65in, 1fr), column-gutter: 14pt,
      [#text(size: 10pt, weight: "bold", fill: wine)[試辦 ≠ 第一個付費市場]],
      [#text(size: 10pt)[若獲同意，臺大可用來驗證流程與安全；商業化仍從最熟悉 BSRS、痛點最明確的心理專科場域開始。]],
    )
  ]
]

#place(bottom + left, dx: margin-x, dy: -0.58in)[
  #text(size: 8.2pt, fill: muted)[場域資訊來源：國立臺灣大學學務處學生心理輔導中心公開服務說明；本案尚未宣稱與臺大建立合作。]
]
#footer(7)
#pagebreak()
