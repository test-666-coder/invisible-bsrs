#import "theme.typ": *

#let roadmap-columns = (1.55fr, 4.35fr, 2.05fr, 2.05fr)

#let gate-row(period, title, subtitle, action, evidence, stop, fill: white) = block(
  width: content-w,
  height: 0.93in,
  fill: fill,
  radius: 7pt,
  inset: (x: 12pt, y: 8pt),
)[
  #grid(columns: roadmap-columns, column-gutter: 14pt,
    [
      #grid(columns: (auto, 1fr), column-gutter: 8pt,
        box(fill: wine, radius: 10pt, inset: (x: 9pt, y: 3pt))[
          #text(size: 8pt, weight: "bold", fill: white)[#period]
        ],
        text(size: 12pt, weight: "bold")[#title],
      )
      #v(0.04in)
      #text(size: 7.8pt, fill: muted)[#subtitle]
    ],
    [#text(size: 8.8pt)[#action]],
    block(stroke: (left: 0.8pt + sand), inset: (left: 11pt))[
      #text(size: 8pt, weight: "bold", fill: wine)[達標]
      #v(0.04in)
      #text(size: 8.4pt)[#evidence]
    ],
    block(stroke: (left: 0.8pt + sand), inset: (left: 11pt))[
      #text(size: 8pt, weight: "bold", fill: wine)[停下]
      #v(0.04in)
      #text(size: 8.4pt, fill: muted)[#stop]
    ],
  )
]

#head("附錄", "落地計畫｜四階段驗證，不達標就停", "附錄二 · 從測試走到付費", "A2")

#place(left + top, dx: margin-x, dy: 1.30in)[
  #block(width: content-w, fill: blush, radius: 7pt, inset: (x: 14pt, y: 9pt))[
    #grid(columns: (0.9in, 1fr), column-gutter: 10pt, row-gutter: 4pt,
      [#text(size: 8.5pt, weight: "bold", fill: wine)[核心原則]],
      [#text(size: 8.7pt)[每一階段都先驗證，再決定是否投入下一步；臺大是目標驗證場域，目前尚未合作。]],
      [#text(size: 8.5pt, weight: "bold", fill: wine)[擴張順序]],
      [#text(size: 8.7pt)[先做出台灣可行模式，再一次進入一個國家；不同地區都要重新完成專業與法規驗證。]],
    )
  ]
]

#place(left + top, dx: margin-x, dy: 1.93in)[
  #block(width: content-w, inset: (x: 12pt, y: 0pt))[
    #grid(columns: roadmap-columns, column-gutter: 14pt,
      [#text(size: 7.8pt, weight: "bold", fill: muted)[時間與目標]],
      [#text(size: 7.8pt, weight: "bold", fill: muted)[這一階段要做什麼]],
      [#text(size: 7.8pt, weight: "bold", fill: muted)[做到什麼才前進]],
      [#text(size: 7.8pt, weight: "bold", fill: muted)[什麼情況要停]],
    )
  ]
]

#place(left + top, dx: margin-x, dy: 2.18in)[
  #grid(columns: (content-w,), rows: (0.93in, 0.93in, 0.93in, 0.93in), row-gutter: 0.10in,
    gate-row(
      "0–3 月",
      "準備與測試",
      "先證明系統不亂判斷",
      [取得量表使用授權；請 2–3 位心理師共同訂規則，準備至少 200 件模擬或去識別案例，並接洽至少 3 個可能的合作場域。],
      [高風險線索找對至少 95% #linebreak() 每個判斷都能回到原文],
      [連續兩輪未達標 #linebreak() → 縮小功能範圍],
    ),
    gate-row(
      "4–9 月",
      "小規模試辦",
      "先讓心理師測試，不影響真實決策",
      [取得合作意向與校內負責人；完成研究倫理、個資、資安審查，並確認是否屬醫療器材，再由 3–5 位心理師測試約 100 件案例。],
      [沒有重大事故 #linebreak() 至少 70% 認為有用｜覆核不超過 2 分鐘],
      [審查未完成或發生重大問題 #linebreak() → 立即停試],
      fill: blush,
    ),
    gate-row(
      "10–18 月",
      "付費驗證",
      "證明有人願意持續付費",
      [找 3 家機構進行付費試用；由心理師共同建立並審核專業知識庫，觀察是否真的節省整理時間，並確認持續使用意願。],
      [至少 2 家續約 #linebreak() 一半試用機構願意付費],
      [沒有持續使用或不願付費 #linebreak() → 重新確認客戶痛點],
      fill: blush,
    ),
    gate-row(
      "18–36 月",
      "海外試辦",
      "一次只進入一個國家",
      [台灣模式穩定後，只選一個國家；與當地心理師及法規夥伴重建專業知識庫、危機轉介資源與在地測試案例。],
      [達到台灣相同安全標準 #linebreak() 1 個在地夥伴｜2 個付費試辦],
      [缺少法規、專家或轉介資源 #linebreak() → 不正式上線],
      fill: sand,
    ),
  )
]

#place(left + top, dx: margin-x, dy: 6.38in)[
  #block(width: content-w, fill: wine, radius: 7pt, inset: (x: 13pt, y: 8pt))[
    #grid(columns: (0.68in, 1fr, 1fr, 1fr, 1fr), column-gutter: 10pt,
      [#text(size: 8.3pt, weight: "bold", fill: white)[現況]],
      [#text(size: 8.3pt, fill: white)[已完成｜原型與本機流程]],
      [#text(size: 8.3pt, fill: white)[待驗證｜安全、工作流、付費]],
      [#text(size: 8.3pt, fill: white)[待取得｜合作、審查、付費]],
      [#text(size: 8.3pt, fill: white)[明確不做｜自動診斷或取代心理師]],
    )
  ]
]

#place(left + top, dx: margin-x, dy: 6.92in)[
  #text(size: 7.6pt, fill: muted)[頁面中的數字是提案階段的驗收目標；正式試辦前，仍須與合作心理師及校方共同確認。]
]

#footer("A2")
