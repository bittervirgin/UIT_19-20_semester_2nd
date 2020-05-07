#pragma once
#include <afxwin.h>
class Cline
{
public:
	static void LineDDA(CDC* pDC, CPoint A, CPoint B, COLORREF color);
	static void LineDDA(CDC* pDC, int x1, int y1, int x2, int y2, COLORREF color);
	static void Bressenham(CDC* pDC, int x1, int y1, int x2, int y2, COLORREF color);
	static void MidPoint(CDC* pDC, float r, COLORREF color);
private:
	//Duong tang cham, giam cham - lap theo xs
	static void _LineDDA1(CDC* PDC, int x1, int y1, int x2, int y2, COLORREF color);
	//DUong tang nhanh va giam nhanh - lap theo y
	static void _LineDDA2(CDC* pDC, int x1, int y1, int x2, int y2, COLORREF color);
	//Bressenham
	static void _Bressenham1(CDC* pDC, int x1, int y1, int x2, int y2, COLORREF color);
	static void _Bressenham2(CDC* pDC, int x1, int y1, int x2, int y2, COLORREF color);
	static void _MidPoint(CDC* pDC, float r, COLORREF color);
};

