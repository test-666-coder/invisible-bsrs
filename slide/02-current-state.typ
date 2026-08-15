#import "theme.typ": *

#head("壹", "現況分析與 TA 分析", "CURRENT STATE · TARGET AUDIENCE", 2)

#place(left + top, dx: margin-x, dy: content-y)[
  #deck-grid(columns: (1.38fr, 0.82fr), gutter: gap,
    panel([
      #tag("核心痛點")
      #v(0.2in)
      #text(size: 22pt, weight: "bold")[自陳量表的盲點：患者必須先願意承認]
      #v(0.16in)
      #text(size: 13pt, fill: muted)[BSRS 需要患者自行填答；但受到自我認知、防衛或污名影響，答案未必呈現完整狀態。]
      #v(0.2in)

      #grid(columns: (1fr, 0.32in, 1fr), gutter: 9pt,
        block(fill: cream, radius: 6pt, inset: 14pt, height: 1.95in)[
          #text(size: 11pt, weight: "bold", fill: muted)[量表上的回答]
          #v(0.13in)
          #text(size: 15pt, weight: "bold")[過去一週，您是否容易動怒？]
          #v(0.03in)
          #box(width: 100%, fill: white, radius: 4pt, stroke: 1pt + sand, inset: 12pt)[
            #grid(columns: (18pt, 1fr), column-gutter: 8pt,
              circle(radius: 7pt, stroke: 1.5pt + muted),
              text(size: 15pt)[沒有，我還好]
            )
          ]
        ],
        align(center + horizon)[#text(size: 27pt, weight: "bold", fill: wine)[≠]],
        block(fill: blush, radius: 6pt, inset: 14pt, height: 1.95in)[
          #text(size: 11pt, weight: "bold", fill: wine)[自然對話中的訊號]
          #v(0.13in)
          #text(size: 21pt, weight: "bold", fill: wine)[「最近一點小事，就讓我很火大。」]
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

#place(bottom + left, dx: margin-x, dy: -0.62in)[
  #text(size: 18pt, weight: "bold", fill: wine)[不是患者沒有症狀，而是症狀未必會被自己填進量表。]
]
#footer(2)
#pagebreak()
