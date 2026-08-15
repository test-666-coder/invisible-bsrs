#import "theme.typ": *

#head("伍", "市場、商業模式與競爭", "CUSTOMER · REVENUE · DIFFERENTIATION", 6)
#place(left + top, dx: margin-x, dy: content-y)[
  #deck-grid(columns: (1fr, 1fr, 1fr), gutter: gap,
    panel([#tag("市場切入") #v(0.22in) #text(size: 19pt, weight: "bold")[先從高需求場域開始] #v(0.16in) #bullet[精神科／身心科門診] #v(0.1in) #bullet[心理諮商與家醫科] #v(0.1in) #bullet[學校輔導中心]], fill: white, height: 4.82in),
    panel([#tag("商業模式") #v(0.22in) #text(size: 19pt, weight: "bold")[依規模與整合深度收費] #v(0.16in) #bullet[SaaS 帳號／據點／時數訂閱] #v(0.1in) #bullet[HIS、EMR API 授權] #v(0.1in) #bullet[大型院所私有部署]], fill: white, height: 4.82in),
    panel([#tag("競爭差異") #v(0.22in) #text(size: 19pt, weight: "bold")[補強現行流程，不取代它] #v(0.16in) #bullet[比純問卷更貼近自然敘事] #v(0.1in) #bullet[比人工筆記更易回溯原話] #v(0.1in) #bullet[以人工確認守住臨床界線]], fill: blush, height: 4.82in)
  )
]
#place(bottom + left, dx: margin-x, dy: -0.62in)[#text(size: 16.5pt, weight: "bold", fill: wine)[定位：可追溯的評估草稿層，介於自然對話與正式臨床判斷之間。]]
#footer(6)
#pagebreak()
