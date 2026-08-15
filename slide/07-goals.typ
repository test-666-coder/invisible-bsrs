#import "theme.typ": *

#head("陸", "短長期目標", "VALIDATE FIRST · INTEGRATE NEXT", 7)
#place(left + top, dx: margin-x, dy: content-y)[
  #deck-grid(columns: (1fr, 1fr), gutter: gap,
    panel([#tag("短期｜驗證可用性") #v(0.28in) #text(size: 22pt, weight: "bold", fill: wine)[從概念 Demo 走向封閉式試辦] #v(0.2in) #bullet[完成逐字稿、證據引用與量表介面] #v(0.12in) #bullet[建立標註測試集，檢驗漏報與誤報] #v(0.12in) #bullet[邀請臨床、法規、資安與個資專家審查] #v(0.12in) #bullet[規劃倫理審查核准的封閉式試辦]], fill: white, height: 4.95in),
    panel([#tag("長期｜整合與擴展") #v(0.28in) #text(size: 22pt, weight: "bold", fill: wine)[以證據支持產品導入與宣稱] #v(0.2in) #bullet[串接 HIS／EMR 與院所權限系統] #v(0.12in) #bullet[建立版本、稽核與事件應變機制] #v(0.12in) #bullet[驗證不同語言、口音與族群偏差] #v(0.12in) #bullet[依臨床證據調整產品定位與效益宣稱]], fill: blush, height: 4.95in)
  )
]
#footer(7)
#pagebreak()
