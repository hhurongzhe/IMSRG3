CC = g++
CXX = g++

SRC_DIR   := src
BUILD_DIR := build
OBJ_DIR   := $(BUILD_DIR)/obj
OPT_PREFIX := /Users/mac/Desktop/opt_setup/opt
BOOST_PREFIX := $(OPT_PREFIX)/boost
GSL_PREFIX := $(OPT_PREFIX)/gsl
OPENBLAS_PREFIX := $(OPT_PREFIX)/openblas

LOCAL_INCLUDE_DIRS := $(BOOST_PREFIX)/include $(GSL_PREFIX)/include $(OPENBLAS_PREFIX)/include
LOCAL_LIB_DIRS := $(BOOST_PREFIX)/lib $(GSL_PREFIX)/lib $(OPENBLAS_PREFIX)/lib
comma := ,

INCLUDE   = -I$(SRC_DIR) -Iextern/armadillo -Iextern/half/include $(addprefix -I,$(LOCAL_INCLUDE_DIRS))
FLAGS     = -fPIC -O3 -fopenmp -march=native -std=c++17 -DNO_HDF5
DEPFLAGS  = -MMD -MP
LDFLAGS   = $(addprefix -L,$(LOCAL_LIB_DIRS)) $(foreach dir,$(LOCAL_LIB_DIRS),-Wl$(comma)-rpath$(comma)$(dir))
LIBS      = -lboost_iostreams -lgsl -lgslcblas -lopenblas -lm -lz
SOFLAGS   = -shared $(FLAGS)
PYTHON_CONFIG ?= python3-config
PYTHON ?= python3
PYTHON_INCLUDE = -Iextern/pybind11/include
PYTHON_CFLAGS = $(filter-out -arch arm64 x86_64,$(shell $(PYTHON_CONFIG) --cflags))
PYTHON_LDFLAGS = $(shell $(PYTHON_CONFIG) --ldflags)
STUBGEN_FLAGS = --ignore-invalid-expressions '.*'

ALL = $(BUILD_DIR)/libIMSRG.so $(BUILD_DIR)/imsrg++ $(BUILD_DIR)/pyIMSRG.so

# --- 操作系统检测与路径设置 ---
UNAME_S := $(shell uname -s)
ifeq ($(UNAME_S), Darwin) # macOS 系统
	CC = g++-15
	CXX = g++-15
	FLAGS += -DNO_x86
	# GCC's built-in SDK path may be stale after a Command Line Tools update.
	MACOS_SDK := $(shell xcrun --sdk macosx --show-sdk-path)
	FLAGS += -isysroot "$(MACOS_SDK)"
	PYTHON_LDFLAGS += -undefined dynamic_lookup
	ALL += $(BUILD_DIR)/pyIMSRG/__init__.pyi
endif

.PHONY: all clean python stubs

all: $(ALL)
python: $(BUILD_DIR)/pyIMSRG.so
ifeq ($(UNAME_S), Darwin)
stubs: $(BUILD_DIR)/pyIMSRG/__init__.pyi
else
stubs:
	@echo "pyIMSRG stubs are only generated on macOS."
endif

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
PYIMSRG_OBJ = $(OBJ_DIR)/pyIMSRG.o
DEP = $(OBJ:.o=.d) $(MAIN_OBJ:.o=.d) $(PYIMSRG_OBJ:.o=.d)

$(OBJ_DIR)/%.o: $(SRC_DIR)/%.cc | $(OBJ_DIR)
	$(CXX) -c $< -o $@ $(INCLUDE) $(FLAGS) $(DEPFLAGS)

$(PYIMSRG_OBJ): $(SRC_DIR)/pyIMSRG.cc | $(OBJ_DIR)
	$(CXX) -c $< -o $@ $(INCLUDE) $(PYTHON_INCLUDE) $(FLAGS) $(PYTHON_CFLAGS) $(DEPFLAGS)

$(BUILD_DIR)/libIMSRG.so: $(OBJ) | $(BUILD_DIR)
	$(CXX) $^ $(SOFLAGS) -o $@ $(LDFLAGS) $(LIBS)

$(BUILD_DIR)/imsrg++: $(MAIN_OBJ) $(BUILD_DIR)/libIMSRG.so | $(BUILD_DIR)
	$(CXX) $< -o $@ $(FLAGS) -L$(BUILD_DIR) -lIMSRG $(LDFLAGS) $(LIBS)

$(BUILD_DIR)/pyIMSRG.so: $(OBJ) $(PYIMSRG_OBJ) | $(BUILD_DIR)
	$(CXX) $^ $(SOFLAGS) -o $@ $(LDFLAGS) $(PYTHON_LDFLAGS) $(LIBS)

$(BUILD_DIR)/pyIMSRG/__init__.pyi: $(BUILD_DIR)/pyIMSRG.so | $(BUILD_DIR)
	cd $(BUILD_DIR) && $(PYTHON) -m pybind11_stubgen pyIMSRG -o . $(STUBGEN_FLAGS)

$(BUILD_DIR) $(OBJ_DIR):
	mkdir -p $@

clean:
	rm -rf $(BUILD_DIR)

-include $(DEP)
