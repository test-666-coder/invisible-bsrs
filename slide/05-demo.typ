#import "theme.typ": *

#head("肆", "Demo", "FROM NATURAL SPEECH TO REVIEWABLE EVIDENCE", 5)
#place(left + top, dx: margin-x, dy: content-y)[
  #deck-grid(columns: (4.0in, 0.5in, 1fr), gutter: gap,
    panel([#tag("診間自然對話") #v(0.25in) #text(size: 24pt, weight: "bold")[「最近晚上都睡不好，小孩稍微吵一下我就想罵人，覺得自己是個很糟糕的媽媽……」] #v(0.3in) #text(size: 12.5pt, fill: muted)[患者不必先理解量表，也不必離開原本的敘事脈絡。]], fill: white, height: 4.95in),
    align(center + horizon)[#text(size: 38pt, fill: wine)[→]],
    panel([
      #grid(columns: (1fr, 1fr, 1fr), gutter: 10pt,
        ..(("睡眠困難", "3", "高"), ("易怒", "3", "高"), ("自卑", "2", "中")).map(((name, score, conf)) => block(fill: cream, radius: 5pt, inset: 12pt)[#text(size: 12pt, fill: muted)[#name] #linebreak() #text(size: 28pt, weight: "bold", fill: wine)[#score] #text(size: 10pt, fill: muted, [／4 · 信心 ] + conf)]))
      #v(0.2in) #text(size: 15pt, weight: "bold")[原文證據] #v(0.08in)
      #box(width: 100%, fill: blush, radius: 5pt, inset: 13pt)[#text(size: 14pt)[「最近晚上都睡不好」 → 睡眠困難]] #v(0.11in)
      #box(width: 100%, fill: blush, radius: 5pt, inset: 13pt)[#text(size: 14pt)[「覺得自己是個很糟糕的媽媽」 → 自卑]] #v(0.18in)
      #tag("待醫療人員確認", fill: wine)
    ], fill: white, height: 4.95in)
  )
]
#place(bottom + left, dx: margin-x, dy: -0.6in)[#text(size: 17pt, weight: "bold", fill: wine)[不硬猜：證據不足就標示「資訊不足」，而不是補出一個分數。]]
#footer(5)
#pagebreak()
