/* ==========================================================================
 *
 * Author's comments
 *
 * samlib.h
 *
 * ==========================================================================
 */

#ifndef H_SAMLIB
#define H_SAMLIB

#include <Python.h>

#include <stdio.h>
#include <gsl/gsl_matrix.h>
#include <lfulib.h>
#include <mesh.h>
#include <voxel.h>
#include <geoms.h>
#include <DataFiles.h>
#include <SAMfiles.h>
#include <TimeSegs.h>
#include <nifti1.h>
#include "samutil.h"
#include "sam_param.h"

#define DSDIR "%d/%s"   // default GetFilePath() pattern for files in the ds dir

#define ACTIVE          0
#define CONTROL         1

typedef struct {            // gifti atlas information
    VOXELINFO   *Voxel;     // array of all (indexed) voxels, RH first, then LH
    int         *ridx;      // RH index
    int         *lidx;      // LH index
    int         nrh;        // number of (indexed) voxels on the right
    int         nlh;        // ... and on the left
    void        *meta;      // pointer to gifti metadata
    double      cent[3];    // centroid, from metadata
} GIIATLAS;

void    A5toQ6(double *, FIELD *);
void    A6toQ6(double *, FIELD *);
int     AtoV(double *, unsigned char *, int, double[2][4][4], FIELD *);
double  BSensor(FIELD *Q, SENSOR *Sensor, double *Sp);
int     BestSphere(char *, ChannelInfo *, int, int);
double  blur(FIELD *, SENSOR *, double *, double);
int     CopySensor(SENSOR *, SENSOR *);
int     CtoI(int *, int, int, ChannelInfo *, char **);
void    CtoS(double *Vc, double *Vs);
void    CtoSl(double *, double *);
double  Dflip(void *);
int     DQSolve3D(double Org[3], double *Bt, gsl_matrix *C, HeaderInfo *Header, ChannelInfo *Channel, int Order, double *span);
void    ESum(double *, double *, double *);
void    EtoR(double[3], double[3][3]);
float   Fflip(void *);
int     FitJig(FIELD *, FIELD *, int, XFORM *, double *);
int     FixQ(SNODE *, int, FIELD *, int, int);
float   FloatSwap(float);
double  Forward(FIELD *, SENSOR *, double *);
double  Fwd(FIELD *, SENSOR *, double *, int);
double  Fwd2(FIELD *, SENSOR *, int);
double  FwdLine(FIELD *, double, SENSOR *, int);
int     FwdLineVec(FIELD *, double, double *, ChannelInfo *, int *, int, int, int);
double  FwdM(FIELD *, SENSOR *, int);
int     FwdMVec(FIELD *, double *, HeaderInfo *, ChannelInfo *, int);
void    FwdVec(FIELD *, double *, double *, HeaderInfo *, ChannelInfo *, int);
void    FreeSensor(SENSOR *);
int     GJ(double **, int, double *);
void    GetAtlas(char *PathName, VOXELINFO **Vertex, int *N);
GIIATLAS *GetGiiAtlas(char *AtlasName);
int     GetBad(char *, int **, int *);
int     GetBadSegments(char *, int, int, double, unsigned char ***, int *, int);
void    GetCov(char *, COV_HDR *, int **, gsl_matrix *);
int     GetCov2(char *, COV_HDR *, int *, double **);
void    GetDsInfo(char *, char *, HeaderInfo *, ChannelInfo **, EpochInfo **, unsigned char ***, int);
void    GetDsData(HeaderInfo *, int, int, double, double *);
int     GetCTFData(HeaderInfo *, int, int, double, double *);
int     GetMRIPath(char *path, int len, PyObject *p, char *name);
int     GetFilePath(char *pattern, char *path, int len, PyObject *p, char *name);
int     GetHC(char *, double (*)[3]);
void    GetHDM(char *, HEAD_MODEL *);
void    GetMarkers(char *, SAM_MARKS **, int *);
int     GetMEG(char *, HeaderInfo *, ChannelInfo **, EpochInfo **, long ****, int);
void    GetMesh(char *MeshPath, HULL *Mesh);
void    GetNIFTI(char *ImageName, int *nt, float ***Data, nifti_1_header *Header);
gsl_matrix *GetNIFTIWts(char *WgtFilePath, nifti_1_header *Header, char *Ext, unsigned char **ExtHeader);
gsl_matrix *GetGIFTIWts(char *WgtFilePath);
void    GetNIFTIMask(char *MaskPath, unsigned char **Mask, int *nv);
void    GetNoise(char *dir, char *name, double *r);
void    GetParams(char *, PARMINFO * Params);
void    GetROI(char *PathName, HULL *Hull, VOXELINFO **Vertex, int *);
void    GetROIVertices(VOXELINFO **ROIvertex, char *PathName, int ROInum, int ROIhemi, int *Nvert);
int     GetSpecFile(char *, COV_SPEC **, int *, int *);
void    GetSurfer(char *PathName, VOXELINFO **VoxelList, int *N);
void    GetTargets(char *PathName, VOXELINFO **Target, int *N);
int     GetTmp(char *, long int *, int, int);
int     GetWH2500Data(char *, char *, HeaderInfo *, int, int, double, double *);
int     GetWH2500Info(char *, char *, HeaderInfo *, ChannelInfo **, EpochInfo **);
void    GetVoxels(VOXELINFO **Voxel, int *NumVoxels, HULL * Hull, double Ts[3], double Te[3], double step);
void    GetVoxelsFS(char *Atlas, VOXELINFO **Voxel, int *NumVoxels, double Ts[3], double Te[3], double *step);
void    GetVoxelsHDM(VOXELINFO **Voxel, int *NumVoxels, char *ShapeName, double Ts[3], double Te[3], double step);
void    GetVoxelsHS(VOXELINFO **Voxel, int *NumVoxels, char *RunName, double Ts[3], double Te[3], double step);
void    GetWts(char *, SAM_HDR *, int **, double ***);
void    HStoMS(char *, HeaderInfo *, ChannelInfo *);
int     HullToMS(char *, HeaderInfo *, ChannelInfo *);
double  **InitElect(char *, int *);
PROBE   *InitProbe(char *);
void    ItoC(int *, int, ChannelInfo *, char **);
void    J1toB(double O[3], double S[3], double Sp[3], double L[3][3]);
void    J2toB(double O[3], double S[3], double Sp[3], double L[3][3][3]);
void    JMtoB(double Org[3], double S[3], double Sp[3], double L[12][3]);
int     LeadField(SENSOR *, double *, double *, double *, int, double *);
long    LongSwap(long);
double  LSensor(FIELD *, double, SENSOR *);
int     LSolve(BNODE *, int, FIELD *, double, double *, double *);
void    LtoB(FIELD *, double, FIELD *);
void    LUBackSub(double **, int, int *, double *);
int     LUDecomp(double **, int, int *);
SENSOR  *MakeSensor(PROTO *, FIELD *);
int     ml1(SHAPEINFO *, int, double *, double *, double *);
void    ml2(SHAPEINFO *, int, double *, double **, double *, double *);
void    MLCoeff(SNODE *, int, double *, double **, double *, double *);
void    MLPass(SNODE *, int, double *, double *, double *);
double  MSensor(FIELD *, SENSOR *);
int     MeanVector(SNODE *, int, int, double *, double *);
void    MeshCorr(HeaderInfo *Header, ChannelInfo *NewChannel, gsl_matrix *C, double Noise, HULL *Hull, MESHINFO *Mesh, int N, int *nv, double *Correlation);
void    MeshScatter(HeaderInfo *Header, ChannelInfo *NewChannel, gsl_matrix *C, gsl_matrix *Cinv, double Noise, HULL *Hull, MESHINFO *Mesh, PARMINFO *, int *nv, double *x2, double *slope, double *rms);
void    MeshScatter3(HeaderInfo *Header, ChannelInfo *NewChannel, gsl_matrix *C, double Noise, HULL *Hull, MESHINFO *Mesh, int N, int *nv, double *Correlation, double *rms);
void    MeshScatter2D(HeaderInfo *Header, ChannelInfo *NewChannel, gsl_matrix *C, double Noise, MESHINFO *Mesh, int N, int *nv, double *Correlation);
void    MeshRankScatter(HeaderInfo *Header, ChannelInfo *NewChannel, gsl_matrix *C, double Noise, HULL *Hull, MESHINFO *Mesh, int N, int *nv, double *Correlation, double *rms);
void    MoveField(FIELD *, XFORM *);
void    MoveFrame(HeaderInfo *Header, ChannelInfo *InChannel, ChannelInfo *OutChannel, char *TransFile);
void    MoveMEG(ChannelInfo *, ChannelInfo *, int *, int, XFORM *);
int     MoveProbe(PROBE *, XFORM *);
void    MoveSensor(SENSOR *, XFORM *);
int     MSolve(BNODE *, int, FIELD *, double *);
int     MSolveLoop(BNODE *, int, FIELD *, double, double *, double *);
int     MSolveSensor(SENSOR *, double, FIELD *, double, double *, double *, int, double *);
void    MtoB(FIELD *, FIELD *);
int     MultiLeadField3D(double Org[3], double Vx[3], double **L, HeaderInfo * Header, ChannelInfo * Channel, int Order);
int     MultiSolve3D(double Org[3], double **B, gsl_matrix *C, HeaderInfo * Header, ChannelInfo * Channel, int Order, double *span, int iterate);
double  MutFwd(FIELD *, double, SENSOR *, int);
void    octo(FIELD Org, double dr, double dt, double **Seven);
FILE    *OpenDsFile(HeaderInfo *, char *);
int     OrthoLeadField2D(double Org[3], double **L, double **Pd, double **Pq, HeaderInfo * Header, ChannelInfo * Channel, int Order);
int     OrthoLeadField3D(double Org[3], double **L, double **Pd, double **Pq, HeaderInfo * Header, ChannelInfo * Channel, int Order);
int     OrthoPlane(double *Vr, double *Vx, double *Vy);
void    P5toP6(FIELD *, FIELD *);
void    P6toP5(FIELD *, FIELD *);
void    ParseFileName(char *, char *);
int     ParsePath(char *, char *);
int     PosProbe(PROBE *, char *, int);
double  PredictPoint(SHAPEINFO *, double *);
int     PutCTFData(char *, HeaderInfo *, double, double *);
int     PutMEG(char *, HeaderInfo *, ChannelInfo *, EpochInfo *, long ***);
void    PutCov(char *, COV_HDR *, int *, double **);
void    PutTmp(char *, long int *, int);
void    PutWts(char *WgtPath, gsl_matrix *Wgts, HeaderInfo Header, COV_HDR CovHdr);
void    PutNIFTIImage(float *Image, char *fpath, PARMINFO *Params, char *intent);
void    PutNIFTITargets(char *WgtFilePath, gsl_matrix *Wgt, float Noise);
void    PutNIFTIWts(char *WgtFilePath, PARMINFO *Params, gsl_matrix *Wgt, float Noise);
void    PutGIFTIWts(char *WgtFilePath, gsl_matrix *Wgt, float Noise);
void    PutGIFTISurf(char *surfname, float **d, int nd, int start, int *idx, int n, void *meta, float TimeStep);
int     Q0Solve(SNODE *, int, FIELD *, double *);
int     Q1Solve(SNODE *, int, FIELD *, double *);
void    Q0toB(FIELD *, FIELD *);
double  Q0toV(FIELD *, double *, double);
void    Q6toA5(FIELD *, double *);
int     QAmoeba(FIELD *, SNODE *, int);
void    QGuess(SNODE *, int, FIELD *);
int     QSolve(SNODE *, int, FIELD *, int, int, double *);
int     QStoB(FIELD *, TGLS *, double, FIELD *);
double  QStoV(FIELD *, double *);
void    QtoB(FIELD *, FIELD *, double *);
double  *QtoV(FIELD *, TGLS *, double);
double  QVar(SNODE *, int);
double  QxCorr(SNODE *, int);
COV_SEG *read_segfile(char *name, int *nsegs, HeaderInfo *header);
double  RMSError(SNODE *, int);
double  RMSSignal(SNODE *, int);
void    RSum(double[3][3], double[3][3], double[3][3]);
double  RandomGauss(double, double);
void    RtoE(double[3][3], double[3]);
void    SAM2NIFTIHdr(PARMINFO *Params, int nt, float time_start, float time_step, char *intent_name, int xfm, nifti_1_header *Header);
int     SAMFwd(double **, double *, double, double *, int);
void    SAMsolve(gsl_matrix *C, gsl_matrix *Cinv, gsl_vector *Bp, gsl_vector *Wgt, double noise, double *s2, double *n2);
void    SERvs(double **x, double *vs, double *Bp, int TS, int TE, int M, double tau, double rate, double noise);
void    Shuffle(int *, int);
int     SLSolve(SENSOR *, double *, FIELD *, double, double, double *, double *, int, double *);
int     SSolve(SENSOR *, double *, FIELD *, double *, double *, int, double *);
short   ShortSwap(short);
void    ShowProbe(PROBE *);
int     SolveJoint(gsl_matrix *C, double **B, double *Bp, int rank);
void    Sort(double *, int);
int     StoB(FIELD *, SNODE *, int);
void    StoC(double *, double *);
void    StoCl(double *, double *);

int param_getstr(PyObject *p, char *name, char **);
int param_getint(PyObject *p, char *name, int *);

#endif // H_SAMLIB