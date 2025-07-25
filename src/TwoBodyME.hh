///////////////////////////////////////////////////////////////////////////////////
//    TwoBodyME.hh, part of  imsrg++
//    Copyright (C) 2018  Ragnar Stroberg
//
//    This program is free software; you can redistribute it and/or modify
//    it under the terms of the GNU General Public License as published by
//    the Free Software Foundation; either version 2 of the License, or
//    (at your option) any later version.
//
//    This program is distributed in the hope that it will be useful,
//    but WITHOUT ANY WARRANTY; without even the implied warranty of
//    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
//    GNU General Public License for more details.
//
//    You should have received a copy of the GNU General Public License along
//    with this program; if not, write to the Free Software Foundation, Inc.,
//    51 Franklin Street, Fifth Floor, Boston, MA 02110-1301 USA.
///////////////////////////////////////////////////////////////////////////////////

#ifndef TwoBodyME_h
#define TwoBodyME_h 1

#include "ModelSpace.hh"
#include <array>
#include <fstream>
#include <map>
#include <memory>
class TwoBodyME_ph;

/// The two-body piece of the operator, stored in a vector of maps of of armadillo matrices.
/// The index of the vector indicates the J-coupled two-body channel of the ket state, while the
/// map key is the two-body channel of the bra state. This is done to allow for tensor operators
/// which connect different two-body channels without having to store all possible combinations.
/// In the case of a scalar operator, there is only one map key for the bra state, corresponding
/// to that of the ket state.
/// The normalized J-coupled TBME's are stored in the matrices. However, when the TBME's are
/// accessed by GetTBME(), they are returned as
/// \f$ \tilde{\Gamma}_{ijkl} \equiv \sqrt{(1+\delta_{ij})(1+\delta_{kl})} \Gamma_{ijkl} \f$
/// because the flow equations are derived in terms of \f$ \tilde{\Gamma} \f$.
/// For efficiency, only matrix elements with \f$ i\leq j \f$ and \f$ k\leq l \f$
/// are stored.
/// When performing sums that can be cast as matrix multiplication, we have something
/// of the form
/// \f[
/// \tilde{Z}_{ijkl} \sim \frac{1}{2} \sum_{ab}\tilde{X}_{ijab} \tilde{Y}_{abkl}
/// \f]
/// which may be rewritten as a restricted sum, or matrix multiplication
/// \f[
/// Z_{ijkl} \sim \sum_{a\leq b} X_{ijab} Y_{abkl} = \left( X\cdot Y \right)_{ijkl}
/// \f]
class TwoBodyME
{
  public:
    ModelSpace *modelspace;
    std::map<std::array<size_t, 2>, arma::mat> MatEl;
    size_t nChannels;
    bool hermitian;
    bool antihermitian;
    bool allocated;
    int rank_J;
    int rank_T;
    int parity;

    ~TwoBodyME();
    TwoBodyME();
    TwoBodyME(ModelSpace *);
    TwoBodyME(TwoBodyME_ph &); // Transform a ph operator to pp.
    TwoBodyME(ModelSpace *ms, int rankJ, int rankT, int parity);

    TwoBodyME &operator*=(const double);
    TwoBodyME operator*(const double) const;
    TwoBodyME &operator+=(const TwoBodyME &);
    TwoBodyME &operator-=(const TwoBodyME &);

    //  void Copy(const TwoBodyME&);
    void Allocate();
    void Deallocate();
    bool IsHermitian() { return hermitian; };
    bool IsAntiHermitian() { return antihermitian; };
    bool IsNonHermitian() { return not(hermitian or antihermitian); };
    void SetHermitian();
    void SetAntiHermitian();
    void SetNonHermitian();

    arma::mat &GetMatrix(size_t chbra, size_t chket) { return MatEl.at({chbra, chket}); };
    arma::mat &GetMatrix(size_t ch) { return GetMatrix(ch, ch); };
    arma::mat &GetMatrix(std::array<size_t, 2> a) { return GetMatrix(a[0], a[1]); };
    const arma::mat &GetMatrix(size_t chbra, size_t chket) const { return MatEl.at({chbra, chket}); };
    const arma::mat &GetMatrix(size_t ch) const { return GetMatrix(ch, ch); };

    // TwoBody setter/getters
    double GetTBME(int ch_bra, int ch_ket, int a, int b, int c, int d) const;
    double GetTBME_norm(int ch_bra, int ch_ket, int a, int b, int c, int d) const;
    void SetTBME(int ch_bra, int ch_ket, int a, int b, int c, int d, double tbme);
    void AddToTBME(int ch_bra, int ch_ket, int a, int b, int c, int d, double tbme);
    // This violates hermiticity in a single update by updating a matrix element, but not its conjugate.
    // Use only when you are certain you are also going to update the hermitian conjugate accordingly.
    void AddToTBMENonHermNonNormalized(int ch_bra, int ch_ket, int a, int b, int c, int d, double tbme);
    double GetTBME(int ch_bra, int ch_ket, Ket &bra, Ket &ket) const;
    void SetTBME(int ch_bra, int ch_ket, Ket &bra, Ket &ket, double tbme);
    void AddToTBME(int ch_bra, int ch_ket, Ket &bra, Ket &ket, double tbme);
    double GetTBME_norm(int ch_bra, int ch_ket, int ibra, int iket) const;
    void SetTBME(int ch_bra, int ch_ket, int ibra, int iket, double tbme);
    void AddToTBME(int ch_bra, int ch_ket, int ibra, int iket, double tbme);
    // This violates hermiticity in a single update by updating a matrix element, but not its conjugate.
    // Use only when you are certain you are also going to update the hermitian conjugate accordingly.
    void AddToTBMENonHerm(int ch_bra, int ch_ket, int ibra, int iket, double tbme);
    double GetTBME(int j_bra, int p_bra, int t_bra, int j_ket, int p_ket, int t_ket, Ket &bra, Ket &ket) const;
    void SetTBME(int j_bra, int p_bra, int t_bra, int j_ket, int p_ket, int t_ket, Ket &bra, Ket &ket, double tbme);
    void AddToTBME(int j_bra, int p_bra, int t_bra, int j_ket, int p_ket, int t_ket, Ket &bra, Ket &ket, double tbme);
    double GetTBME(int j_bra, int p_bra, int t_bra, int j_ket, int p_ket, int t_ket, int a, int b, int c, int d) const;
    void SetTBME(int j_bra, int p_bra, int t_bra, int j_ket, int p_ket, int t_ket, int a, int b, int c, int d, double tbme);
    void AddToTBME(int j_bra, int p_bra, int t_bra, int j_ket, int p_ket, int t_ket, int a, int b, int c, int d, double tbme);
    double GetTBME_J(int j_bra, int j_ket, int a, int b, int c, int d) const;
    void SetTBME_J(int j_bra, int j_ket, int a, int b, int c, int d, double tbme);
    void AddToTBME_J(int j_bra, int j_ket, int a, int b, int c, int d, double tbme);
    double GetTBME_J_norm(int j_bra, int j_ket, int a, int b, int c, int d) const;
    void GetTBME_J_norm_twoOps(const TwoBodyME &OtherTBME, int j_bra, int j_ket, int a, int b, int c, int d, double &tbme_this, double &tbme_other) const;

    // Scalar setters/getters for backwards compatibility
    double GetTBME(int ch, int a, int b, int c, int d) const;
    double GetTBME_norm(int ch, int a, int b, int c, int d) const;
    void SetTBME(int ch, int a, int b, int c, int d, double tbme);
    void AddToTBME(int ch, int a, int b, int c, int d, double tbme);
    double GetTBME(int ch, Ket &bra, Ket &ket) const;
    double GetTBME_norm(int ch, Ket &bra, Ket &ket) const;
    void SetTBME(int ch, Ket &bra, Ket &ket, double tbme);
    void AddToTBME(int ch, Ket &bra, Ket &ket, double tbme);
    double GetTBME_norm(int ch, int ibra, int iket) const;
    void SetTBME(int ch, int ibra, int iket, double tbme);
    void AddToTBME(int ch, int ibra, int iket, double tbme);
    double GetTBME(int j, int p, int t, Ket &bra, Ket &ket) const;
    void SetTBME(int j, int p, int t, Ket &bra, Ket &ket, double tbme);
    void AddToTBME(int j, int p, int t, Ket &bra, Ket &ket, double tbme);
    double GetTBME(int j, int p, int t, int a, int b, int c, int d) const;
    double GetTBME_norm(int j, int p, int t, int a, int b, int c, int d) const;
    void SetTBME(int j, int p, int t, int a, int b, int c, int d, double tbme);
    void AddToTBME(int j, int p, int t, int a, int b, int c, int d, double tbme);
    double GetTBME_J(int j, int a, int b, int c, int d) const;
    void SetTBME_J(int j, int a, int b, int c, int d, double tbme);
    void AddToTBME_J(int j, int a, int b, int c, int d, double tbme);

    double GetTBME_J_norm(int j, int a, int b, int c, int d) const;

    void Set_pn_TBME_from_iso(int j, int T, int tz, int a, int b, int c, int d, double tbme);
    double Get_iso_TBME_from_pn(int j, int T, int tz, int a, int b, int c, int d);

    double GetTBMEmonopole(int a, int b, int c, int d) const;
    double GetTBMEmonopole_norm(int a, int b, int c, int d) const;
    double GetTBMEmonopole(Ket &bra, Ket &ket) const;

    //  void   AddToTBME_RelCM(int n1, int l1, int n2, int l2, int L12, int S12, int J12, int T12, int Tz12, int n3, int l3, int n4, int l4, int L34, int S34, int J34, int T34, int Tz34, double Vrel, double Vcm);
    //  vector<pair<int,double>> GetLabFrameKets(int n, int lam, int N, int LAM, int L, int S, int J, int T, int Tz);

    void Erase();
    void Scale(double);
    double Norm() const;
    void Symmetrize();
    void AntiSymmetrize();
    void Eye();
    void PrintAllMatrices() const;
    void PrintMatrix(size_t chbra, size_t chket) const { MatEl.at({chbra, chket}).print(); };
    int Dimension();
    int size();

    void WriteBinary(std::ofstream &);
    void ReadBinary(std::ifstream &);
};

TwoBodyME operator+(const TwoBodyME &lhs, const TwoBodyME &rhs);
TwoBodyME operator-(const TwoBodyME &lhs, const TwoBodyME &rhs);
TwoBodyME operator*(const double lhs, const TwoBodyME &rhs);

#endif
