import type { Metadata } from "next";
import "./globals.css";
import "./dynamic.css";
export const metadata:Metadata={title:"隱形溫度計｜醫病對話 BSRS 輔助評估",description:"以對話證據協助醫療人員完成 BSRS-5 心情溫度計評估。"};
export default function RootLayout({children}:Readonly<{children:React.ReactNode}>){return <html lang="zh-Hant"><body>{children}</body></html>}
