#import "theme.typ": *

#head("柒", "成本分析", "COST DRIVERS · REVENUE LOGIC", 8)
#place(left + top, dx: margin-x, dy: content-y)[
  #deck-grid(columns: (1.25fr, 0.75fr), gutter: gap,
    panel([
      #text(size: 20pt, weight: "bold", fill: wine)[主要成本結構] #v(0.2in)
      #grid(columns: (1fr, 1fr), gutter: 12pt,
        ..(("AI 推論", "語音轉錄與 LLM 分析用量"), ("產品開發", "前端、後端與系統整合"), ("安全合規", "去識別、加密、稽核與審查"), ("維運服務", "監控、客服、模型與提示版本管理")).map(((title, body)) => block(fill: cream, radius: 5pt, inset: 13pt)[#text(size: 15pt, weight: "bold")[#title] #linebreak() #text(size: 12.5pt, fill: muted)[#body]]))
      #v(0.22in)
      #box(width: 100%, fill: blush, radius: 5pt, inset: 14pt)[#text(size: 15pt, weight: "bold", fill: wine)[單位成本公式] #linebreak() #text(size: 14pt)[每月固定成本 ＋ 單次轉錄／分析成本 × 使用量]]
    ], fill: white, height: 4.95in),
    panel([
      #tag("收入對應") #v(0.28in)
      #text(size: 20pt, weight: "bold")[讓收費結構覆蓋不同成本來源] #v(0.2in)
      #bullet[訂閱費支應產品與日常維運] #v(0.12in)
      #bullet[用量費反映 AI 推論成本] #v(0.12in)
      #bullet[整合費涵蓋 HIS／EMR 導入] #v(0.12in)
      #bullet[私有部署另計環境與稽核成本]
      #v(0.3in)
      #text(size: 13pt, fill: muted)[正式定價須在試辦後，依實際使用量、導入工時與院所採購意願驗證。]
    ], fill: sand, height: 4.95in)
  )
]
#footer(8)
#pagebreak()
