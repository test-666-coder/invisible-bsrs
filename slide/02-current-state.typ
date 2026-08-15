#import "theme.typ": *

#head("壹", "現況分析與 TA 分析", "CURRENT STATE · TARGET AUDIENCE", 2)

#place(left + top, dx: margin-x, dy: content-y)[
  #deck-grid(columns: (1.38fr, 0.82fr), gutter: gap,
    panel([
      #tag("現況分析")
      #v(0.18in)
      #grid(columns: (1fr, 1fr), gutter: 12pt,
        block(fill: cream, radius: 6pt, inset: 14pt, height: 3.62in)[
          #text(size: 11pt, weight: "bold", fill: wine)[痛點 01｜患者不一定願意填]
          #v(0.14in)
          #text(size: 18pt, weight: "bold")[自陳量表仰賴主動承認]
          #v(0.13in)
          #text(size: 12pt, fill: muted)[受到自我認知、防衛或污名影響，填答結果未必呈現完整狀態。]
          #v(0.13in)
          #text(size: 12pt, fill: muted)[例如：處於易怒狀態的人可能會不願意承認自己易怒]
        ],
        block(fill: blush, radius: 6pt, inset: 14pt, height: 3.62in)[
          #text(size: 11pt, weight: "bold", fill: wine)[痛點 02｜自殺風險仍需更早看見]
          #v(0.14in)
          #text(size: 17pt, weight: "bold")[台灣每年仍有近四千人死於自殺]
          #v(0.14in)
          #text(size: 34pt, weight: "bold", fill: wine)[3,951]
          #text(size: 11pt, fill: muted)[ 人｜114 年死亡人數]
          #v(0.05in)
          #text(size: 21pt, weight: "bold")[16.9]
          #text(size: 11pt, fill: muted)[ 人／每十萬人口]
          #v(0.1in)
          #text(size: 8.5pt, fill: muted)[資料：衛福部「114 年國人死因統計結果」]
        ]
      )
    ], fill: white, height: 4.95in),

    panel([
      #tag("TA 分析")
      #v(0.13in)
      #text(size: 20pt, weight: "bold", fill: wine)[TA：診所與諮商機構]
      #v(0.11in)

      #box(width: 100%, fill: cream, radius: 5pt, inset: 11pt)[
        #text(size: 13.5pt, weight: "bold")[目標客戶｜診所／諮商機構]
        #v(0.05in)
        #text(size: 12pt, fill: muted)[使用者：醫師、心理師與諮商師]
      ]
      #v(0.09in)
      #box(width: 100%, fill: white, radius: 5pt, inset: 11pt)[
        #text(size: 13.5pt, weight: "bold")[產品輸出｜臨床輔助 Dashboard]
        #v(0.05in)
        #text(size: 12pt, fill: muted)[分析語速、音量與談話內容，整理情緒線索、原文證據與待追問項目]
      ]
    ], fill: blush, height: 4.95in)
  )
]

#footer(2)
#pagebreak()
