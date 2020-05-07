
// Demo_CGView.h : interface of the CDemoCGView class
//

#pragma once


class CDemoCGView : public CView
{
protected: // create from serialization only
	CDemoCGView() noexcept;
	DECLARE_DYNCREATE(CDemoCGView)

// Attributes
public:
	CDemoCGDoc* GetDocument() const;

// Operations
public:

// Overrides
public:
	virtual void OnDraw(CDC* pDC);  // overridden to draw this view
	virtual BOOL PreCreateWindow(CREATESTRUCT& cs);
protected:
	virtual BOOL OnPreparePrinting(CPrintInfo* pInfo);
	virtual void OnBeginPrinting(CDC* pDC, CPrintInfo* pInfo);
	virtual void OnEndPrinting(CDC* pDC, CPrintInfo* pInfo);

// Implementation
public:
	virtual ~CDemoCGView();
#ifdef _DEBUG
	virtual void AssertValid() const;
	virtual void Dump(CDumpContext& dc) const;
#endif

protected:

// Generated message map functions
protected:
	afx_msg void OnFilePrintPreview();
	afx_msg void OnRButtonUp(UINT nFlags, CPoint point);
	afx_msg void OnContextMenu(CWnd* pWnd, CPoint point);
	DECLARE_MESSAGE_MAP()
};

#ifndef _DEBUG  // debug version in Demo_CGView.cpp
inline CDemoCGDoc* CDemoCGView::GetDocument() const
   { return reinterpret_cast<CDemoCGDoc*>(m_pDocument); }
#endif

