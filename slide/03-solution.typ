#import "theme.typ": *

#head("貳", "解決方案", "WHAT THE PRODUCT DOES", 3)

#place(left + top, dx: margin-x, dy: 1.25in)[
  #box(width: content-w, fill: blush, radius: 6pt, inset: (x: 18pt, y: 13pt))[
    #text(size: 23pt, weight: "bold", fill: wine)[把原始語音變成臨床輔助的工具]
    #v(0in)
    #text(size: 15pt, fill: muted)[本地模型處理聲音與個資，校對 Agent 修正逐字稿，最後產出具證據與人工確認欄位的結構化結果。]
  ]
]

#place(left + top, dx: margin-x, dy: 2.72in)[
  #let step-card(no, title, body, foot, fill: white) = panel([
    #grid(
      rows: (0.34in, 0.64in, 1.48in, 0.44in),
      row-gutter: 0.07in,
      tag(no),
      align(left + horizon)[#text(size: 14.5pt, weight: "bold")[#title]],
      align(left + top)[#body],
      align(left + horizon)[
        #box(width: 100%, fill: cream, radius: 4pt, inset: (x: 6pt, y: 6pt))[
          #align(center)[#text(size: 9pt, weight: "bold", fill: wine)[#foot]]
        ]
      ],
    )
  ], fill: fill, height: 3.42in, inset: 14pt)

  #deck-grid(columns: (1fr, 1fr, 1fr, 1fr, 1fr), gutter: 0.12in,
    step-card(
      "01", [本地語音理解],
      [#text(size: 11.5pt)[Whisper 分段轉錄] #v(0.09in)
       #text(size: 11.5pt)[保留時間戳記] #v(0.09in)
       #text(size: 11.5pt)[wav2vec2 情緒 Profile]],
      [音訊留在本機處理],
    ),

    step-card(
      "02", [第一道去識別],
      [#text(size: 11.5pt)[CKIP NER 辨識實體] #v(0.09in)
       #text(size: 11.5pt)[Regex 遮蔽個資] #v(0.09in)
       #text(size: 11.5pt)[轉為安全佔位標籤]],
      [先遮蔽，再進入雲端], fill: blush,
    ),

    step-card(
      "03", [安全校對 Agent],
      [#text(size: 11.5pt)[修正同音字與標點] #v(0.09in)
       #text(size: 11.5pt)[保留遮蔽標籤] #v(0.09in)
       #text(size: 11.5pt)[輸出修改紀錄與警示]],
      [校對後再次去識別],
    ),

    step-card(
      "04", [多模態結構化],
      [#text(size: 11.5pt)[文字＋情緒 Profile] #v(0.09in)
       #text(size: 11.5pt)[BSRS-5 與附加題] #v(0.09in)
       #text(size: 11.5pt)[證據、信心、資訊缺漏]],
      [Schema 1.1.0 強制驗證], fill: blush,
    ),

    step-card(
      "05", [專業覆核輸出],
      [#text(size: 11.5pt)[確認、修改或追問] #v(0.09in)
       #text(size: 11.5pt)[保留模型與 Prompt 版本] #v(0.09in)
       #text(size: 11.5pt)[輸出可稽核 JSON]],
      [正式判斷仍由人完成], fill: sand,
    )
  )
]

#footer(3)
#pagebreak()
