// Homeworks_No3.cpp : This file contains the 'main' function. Program execution begins and ends there.
//

#include <iostream>
#include <glut.h>
#include <gl/GL.h>
#include <gl/GLU.h>


void Init()
{
    glClearColor(0.0, 0.0, 0.0, 0.0);
}

void ReShape(int width, int height)
{
    if (height == 0) {
        height = 1;
    }

    float ratio = (float)width / (float)height;

    glViewport(0, 0, width, height);
    glMatrixMode(GL_PROJECTION);
    glLoadIdentity();
    gluPerspective(45.0, ratio, 0.1, 100.0);
    glMatrixMode(GL_MODELVIEW);
}

void RenderScene()
{
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT);
    glLoadIdentity();
    gluLookAt(0.0, 0.0, 0.5, 0.0, 0.0, 0.0, 0.0, 1.0, 0.0);
    glPushMatrix();
    glRotatef(45.0, 0.0, 0.0, 1.0);
    glColor3f(1.0, 1.5, 0.5);
    glutWireTeapot(0.05);
    glPopMatrix();
    //
    gluLookAt(0.0, 0.0, 2.5, 0.0, 0.0, 0.0, 0.0, 3.0, 0.0);
    glPushMatrix();
    glTranslated(2.0, 0.0, 0.0);
    //DrawCoordinate();
    glColor3f(0.0, 1.0, 0.0);
    glutWireTorus(0.2, 0.5, 5.0, 7.0);
    glPopMatrix();
    //
    gluLookAt(0.0, 0.0, -2.5, 0.0, 0.0, 0.0, 0.0, -3.0, 0.0);
    glPushMatrix();
    glTranslated(-3.0, 0.0, 0.0);
    glRotatef(45.0, -2.0, 1.0, 0.0);
    glColor3f(1.0, 0.0, 1.5);
    glutWireCone(1.5, 3.0, 10.0, 10.0);
    glPopMatrix();

    glutSwapBuffers();
    glFlush();
}

void main()
{
    glutInitDisplayMode(GLUT_DOUBLE | GLUT_RGB);

    glutInitWindowSize(1200, 500);

    glutInitWindowPosition(100, 100);

    glutCreateWindow("Opengl Lab-02");

    Init();

    

    glutReshapeFunc(ReShape);

    glutDisplayFunc(RenderScene);

    glutMainLoop();

}



// Run program: Ctrl + F5 or Debug > Start Without Debugging menu
// Debug program: F5 or Debug > Start Debugging menu

// Tips for Getting Started: 
//   1. Use the Solution Explorer window to add/manage files
//   2. Use the Team Explorer window to connect to source control
//   3. Use the Output window to see build output and other messages
//   4. Use the Error List window to view errors
//   5. Go to Project > Add New Item to create new code files, or Project > Add Existing Item to add existing code files to the project
//   6. In the future, to open this project again, go to File > Open > Project and select the .sln file
