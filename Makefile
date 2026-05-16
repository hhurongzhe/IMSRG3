CC = g++
CXX = g++

SRC_DIR   := src
BUILD_DIR := build
OBJ_DIR   := $(BUILD_DIR)/obj

INCLUDE   = -I$(SRC_DIR) -Iextern/armadillo -Iextern/half/include
FLAGS     = -fPIC -O3 -fopenmp -march=native -std=c++17 -DNO_HDF5
DEPFLAGS  = -MMD -MP
SOFLAGS   = -shared $(FLAGS)

ALL = $(BUILD_DIR)/libIMSRG.so $(BUILD_DIR)/imsrg++

# --- 操作系统检测与路径设置 ---
UNAME_S := $(shell uname -s)
ifeq ($(UNAME_S), Darwin) # macOS 系统
	CC = g++-15
	CXX = g++-15
	LIBS = -lboost_iostreams -lgslcblas -lblas -Xpreprocessor -DNO_x86 -framework Accelerate -lgsl -lm -lz -L/opt/homebrew/opt/gsl/lib -L/opt/boost_gcc15/lib
	INCLUDE += -I/opt/homebrew/opt/gsl/include -I/opt/boost_gcc15/include
else # hrz on .7
	LIBS = -L/opt/library/boost-1.81.0/lib -lboost_iostreams -lopenblas -lgslcblas -lgsl -lz
	INCLUDE += -I/opt/library/boost-1.81.0/include
endif

.PHONY: all clean

all: $(ALL)

OBJ_NAMES = ModelSpace.o TwoBodyME.o ThreeBodyME.o Operator.o ReadWrite.o \
      HartreeFock.o imsrg_util.o Generator.o GeneratorPV.o IMSRGSolver.o IMSRGSolverPV.o \
      BCH.o AngMom.o AngMomCache.o \
      IMSRGProfiler.o \
      Commutator.o Commutator232.o TensorCommutators.o IMSRG3Commutators.o \
      FactorizedDoubleCommutator.o DaggerCommutators.o \
      HFMBPT.o RPA.o \
      M0nu.o Pwd.o DarkMatterNREFT.o Jacobi3BME.o UnitTest.o \
      TwoBodyChannel.o ThreeBodyChannel.o \
      ThreeBodyStorage.o ThreeBodyStorage_pn.o ThreeBodyStorage_iso.o \
      ThreeBodyStorage_no2b.o ThreeBodyStorage_mono.o ThreeLegME.o \
      version.o \
      ReferenceImplementations.o

OBJ = $(addprefix $(OBJ_DIR)/,$(OBJ_NAMES))
MAIN_OBJ = $(OBJ_DIR)/imsrg++.o
DEP = $(OBJ:.o=.d) $(MAIN_OBJ:.o=.d)

$(OBJ_DIR)/%.o: $(SRC_DIR)/%.cc | $(OBJ_DIR)
	$(CXX) -c $< -o $@ $(INCLUDE) $(FLAGS) $(DEPFLAGS)

$(BUILD_DIR)/libIMSRG.so: $(OBJ) | $(BUILD_DIR)
	$(CXX) $^ $(SOFLAGS) -o $@ $(LIBS)

$(BUILD_DIR)/imsrg++: $(MAIN_OBJ) $(BUILD_DIR)/libIMSRG.so | $(BUILD_DIR)
	$(CXX) $< -o $@ $(FLAGS) -L$(BUILD_DIR) -lIMSRG $(LIBS)

$(BUILD_DIR) $(OBJ_DIR):
	mkdir -p $@

clean:
	rm -rf $(BUILD_DIR)

-include $(DEP)
