#include "pch.h"
#include "CLine.h"

#define Round(x) (int) (x + 0.5)

void Cline::LineDDA(CDC* pDC, CPoint A, CPoint B, COLORREF color)
{
	LineDDA(pDC, A.x, A.y, B.x, B.y, color);
}

void Cline::LineDDA(CDC* pDC, int x1, int y1, int x2, int y2, COLORREF color)
{
	//Neu 2 diem x1, y1 trung x2, y2 -> Chi ve 1 diem
	if (x1 == x2 && y1 == y2) {
		pDC->SetPixel(x1, y1, color);
		return;
	}
	//Khong trung nhau
	//Kiem tra xem tang/giam cham/nhanh
	if (abs(x2 - x1) >= abs(y2 - y1)) {
		//Kiem tra diem dau
		if (x1 <= x2) {
			_LineDDA1(pDC, x1, y1, x2, y2, color);
		}
		else {
			_LineDDA1(pDC, x2, y2, x1, y1, color);
		}			
	}
	else {
		if (y1 < y2) {
			_LineDDA2(pDC, x1, y1, x2, y2, color);
		}
		else {
			_LineDDA2(pDC, x2, y2, x1, y1, color);
		}
	}

}

void Cline::_LineDDA1(CDC* pDC, int x1, int y1, int x2, int y2, COLORREF color)
{
	//First point
	pDC->SetPixel(x1, y1, color);
	float m = (float)(y2 - y1) / (x2 - x1);
	float y = y1;
	while (x1 < x2) {
		x1 += 1;
		y += m;
		pDC->SetPixel(x1, Round(y), color);
		
	}
}

void Cline::_LineDDA2(CDC* pDC, int x1, int y1, int x2, int y2, COLORREF color)
{
	pDC->SetPixel(x1, x2, color);
	float k = (float)(x2 - x1) / (y2 - y1);
	float x = x1;
	while (y1 < y2) {
		y1 += 1;
		x = x + k;
		pDC->SetPixel(Round(x), y1, color);
	}
}

void Cline::_Bressenham1(CDC* pDC, int x1, int y1, int x2, int y2, COLORREF color)
{
	int p = 2 * (y2 - y1) - (x2 - x1);
	int x = x1;
	int y = y1;
	while (x < x2) {
		if (p < 0) {
			x = x + 1;
			p += (y2 - y1);
		}
		else {
			x += 1;
			y += 1;
			p += 2 * (y2 - y1) - 2 * (x2 - x1);
		}
		pDC->SetPixel(x, y, color);
	}
}

void Cline::_Bressenham2(CDC* pDC, int x1, int y1, int x2, int y2, COLORREF color)
{
	int p = 2 * (y2 - y1) - (x2 - x1);
	int x = x1;
	int y = y1;
	while (x < x2) {
		if (p < 0) {
			y += 1;
			p += 2*(x2 - x1);
		}
		else {
			x += 1;
			y += 1;
			p += 2 * (x2 - x1) - 2 * (y2 - y1);
		}
		pDC->SetPixel(x, y, color);
	}
}

void Cline::Bressenham(CDC* pDC, int x1, int y1, int x2, int y2, COLORREF color)
{
	if (x1 == x2 && y1 == y2) {
		pDC->SetPixel(x1, y1, color);
		return;
	}
	//Khong trung nhau
	//TH1
	if (abs(x2 - x1) >= abs(y2 - y1)) {
		if (x1 <= x2) {
			_Bressenham1(pDC, x1, y1, x2, y2, color);
		}
		else {
			_Bressenham1(pDC, x2, y2, x1, y1, color);
		}
	}
	else {
		if (y1 < y2) {
			_Bressenham2(pDC, x1, y1, x2, y2, color);
		}
		else {
			_Bressenham2(pDC, x2, y2, x1, y1, color);
		}
	}
}

void Cline::_MidPoint(CDC* pDC, float r, COLORREF color)
{
	float y = r;
	float x = 0;
	float f = 1 - r;
	while (x < y) {
		if (f < 0) {
			x += 1;
			f = f + 2 * x + 3;
		}
		else {
			x += 1;
			y = y - 1;
			f = f + 2 * (x - y) + 5;
		}
		pDC->SetPixel(Round(x), Round(y), color);
	}

}

void Cline::MidPoint(CDC* pDC, float r, COLORREF color)
{
	MidPoint(pDC, r, color);
}
