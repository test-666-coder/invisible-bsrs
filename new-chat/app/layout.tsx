import type { Metadata } from "next";
import "./globals.css";
import "./dynamic.css";
export const metadata:Metadata={title:"澄心｜AI 情緒聽診器",description:"以對話證據協助醫療人員完成 BSRS-5 心情溫度計評估。"};
export default function RootLayout({children}:Readonly<{children:React.ReactNode}>){return <html lang="zh-Hant"><body>{children}</body></html>}
