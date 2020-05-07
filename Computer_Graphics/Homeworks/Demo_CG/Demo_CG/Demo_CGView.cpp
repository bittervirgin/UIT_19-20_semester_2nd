
// Demo_CGView.cpp : implementation of the CDemoCGView class
//

#include "pch.h"
#include "framework.h"
// SHARED_HANDLERS can be defined in an ATL project implementing preview, thumbnail
// and search filter handlers and allows sharing of document code with that project.
#ifndef SHARED_HANDLERS
#include "Demo_CG.h"
#endif

#include "Demo_CGDoc.h"
#include "Demo_CGView.h"

#ifdef _DEBUG
#define new DEBUG_NEW
#endif
#include "CLine.h"

// CDemoCGView

IMPLEMENT_DYNCREATE(CDemoCGView, CView)

BEGIN_MESSAGE_MAP(CDemoCGView, CView)
	// Standard printing commands
	ON_COMMAND(ID_FILE_PRINT, &CView::OnFilePrint)
	ON_COMMAND(ID_FILE_PRINT_DIRECT, &CView::OnFilePrint)
	ON_COMMAND(ID_FILE_PRINT_PREVIEW, &CDemoCGView::OnFilePrintPreview)
	ON_WM_CONTEXTMENU()
	ON_WM_RBUTTONUP()
END_MESSAGE_MAP()

// CDemoCGView construction/destruction

CDemoCGView::CDemoCGView() noexcept
{
	// TODO: add construction code here

}

CDemoCGView::~CDemoCGView()
{
}

BOOL CDemoCGView::PreCreateWindow(CREATESTRUCT& cs)
{
	// TODO: Modify the Window class or styles here by modifying
	//  the CREATESTRUCT cs

	return CView::PreCreateWindow(cs);
}

// CDemoCGView drawing

void CDemoCGView::OnDraw(CDC* pDC)
{
	CDemoCGDoc* pDoc = GetDocument();
	ASSERT_VALID(pDoc);
	if (!pDoc)
		return;

	// TODO: add draw code for native data here
	Cline::LineDDA(pDC, 0, 0, 1000, 200, RGB(255,0,0));
	Cline::Bressenham(pDC, 0, 0, 1000, 200, RGB(0, 255, 0));
	Cline::Bressenham(pDC, 0, 0, 200, 2000, RGB(0, 255, 0));
	Cline::MidPoint(pDC, 100.0, RGB(0, 0, 200));
}


// CDemoCGView printing


void CDemoCGView::OnFilePrintPreview()
{
#ifndef SHARED_HANDLERS
	AFXPrintPreview(this);
#endif
}

BOOL CDemoCGView::OnPreparePrinting(CPrintInfo* pInfo)
{
	// default preparation
	return DoPreparePrinting(pInfo);
}

void CDemoCGView::OnBeginPrinting(CDC* /*pDC*/, CPrintInfo* /*pInfo*/)
{
	// TODO: add extra initialization before printing
}

void CDemoCGView::OnEndPrinting(CDC* /*pDC*/, CPrintInfo* /*pInfo*/)
{
	// TODO: add cleanup after printing
}

void CDemoCGView::OnRButtonUp(UINT /* nFlags */, CPoint point)
{
	ClientToScreen(&point);
	OnContextMenu(this, point);
}

void CDemoCGView::OnContextMenu(CWnd* /* pWnd */, CPoint point)
{
#ifndef SHARED_HANDLERS
	theApp.GetContextMenuManager()->ShowPopupMenu(IDR_POPUP_EDIT, point.x, point.y, this, TRUE);
#endif
}


// CDemoCGView diagnostics

#ifdef _DEBUG
void CDemoCGView::AssertValid() const
{
	CView::AssertValid();
}

void CDemoCGView::Dump(CDumpContext& dc) const
{
	CView::Dump(dc);
}

CDemoCGDoc* CDemoCGView::GetDocument() const // non-debug version is inline
{
	ASSERT(m_pDocument->IsKindOf(RUNTIME_CLASS(CDemoCGDoc)));
	return (CDemoCGDoc*)m_pDocument;
}
#endif //_DEBUG


// CDemoCGView message handlers
