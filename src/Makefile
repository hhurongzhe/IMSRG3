CXX := g++-15
CXXSTD := c++17

# --- 操作系统检测与路径设置 ---
UNAME_S := $(shell uname -s)

ifeq ($(UNAME_S), Darwin) # macOS 系统
	BOOST_HOME    := /opt/boost_gcc15
	GSL_HOME      := /opt/homebrew/opt/gsl
	OPENBLAS_HOME := /opt/homebrew/opt/openblas
else # 未名2号中boost路径比较奇怪
	BOOST_HOME    := -I/lustre/software/boost/1.77.0
	GSL_HOME      :=
	OPENBLAS_HOME :=
endif

# --- Installation Directory ---
INSTDIR := ../usr

# --- External Dependencies Directory ---
EXTERN := ../extern


# --- Compiler Flags and Definitions
FLAGS := -O3 -march=native -std=$(CXXSTD) -fopenmp -fPIC

# --- Pre-processor Definitions ---
DEFINES := -DNO_HDF5 -DOPENBLAS_NOUSEOMP=1
WARNFLAGS :=
CXXFLAGS := $(FLAGS) $(WARNFLAGS) $(DEFINES)

# =========================================================================
# Include and Library Paths
# =========================================================================

INCLUDE_PATHS := -I$(EXTERN)/armadillo -I$(EXTERN)/half/include
INCLUDE_PATHS += -I$(BOOST_HOME)/include -I$(GSL_HOME)/include

LIBRARY_PATHS := -L$(PWD)
LIBRARY_PATHS += -L$(BOOST_HOME)/lib -L$(GSL_HOME)/lib -L$(OPENBLAS_HOME)/lib

LIBS := -lopenblas -lgsl -lz

# =========================================================================
# OS-Specific Settings (Linux / macOS)
# =========================================================================

OS := $(shell uname -s)

ifeq ($(OS), Darwin)
    CXXFLAGS := -Xpreprocessor $(CXXFLAGS)
    CXXFLAGS += -DNO_x86
    SOFLAGS := -dynamiclib -install_name $(INSTDIR)/lib/libIMSRG.so
    LIBS += -fopenmp
else
    SOFLAGS := -shared
    LIBS +=
endif

# =========================================================================
# Source Files and Targets
# =========================================================================

TARGET_LIB := libIMSRG.so
TARGET_EXE := imsrg++

BOOST_SRC_DIR := $(EXTERN)/boost_src

OBJ_FILES := ModelSpace.o TwoBodyME.o ThreeBodyME.o Operator.o ReadWrite.o \
             HartreeFock.o imsrg_util.o Generator.o GeneratorPV.o IMSRGSolver.o IMSRGSolverPV.o AngMom.o AngMomCache.o \
             IMSRGProfiler.o \
             BCH.o Commutator.o TensorCommutators.o IMSRG3Commutators.o DaggerCommutators.o FactorizedDoubleCommutator.o \
             HFMBPT.o RPA.o \
             M0nu.o DarkMatterNREFT.o Jacobi3BME.o UnitTest.o \
             TwoBodyChannel.o ThreeBodyChannel.o \
             ThreeBodyStorage.o ThreeBodyStorage_pn.o ThreeBodyStorage_iso.o \
             ThreeBodyStorage_no2b.o ThreeBodyStorage_mono.o ThreeLegME.o \
             ReferenceImplementations.o version.o

BOOST_OBJS := $(BOOST_SRC_DIR)/gzip.o $(BOOST_SRC_DIR)/zlib.o

ALL_OBJS := $(OBJ_FILES) $(BOOST_OBJS)

# =========================================================================
# Build Rules
# =========================================================================
.PHONY: all clean install splashscreen

all: $(TARGET_LIB) $(TARGET_EXE)
	@echo "Build complete."

$(TARGET_LIB): $(ALL_OBJS)
	@echo "Linking shared library: $@"
	$(CXX) $^ $(SOFLAGS) -o $@ $(LIBRARY_PATHS) $(LIBS)

$(TARGET_EXE): imsrg++.cc $(TARGET_LIB)
	@echo "Linking executable: $@"
	$(CXX) $(CXXFLAGS) $(INCLUDE_PATHS) $< -o $@ $(LIBRARY_PATHS) -lIMSRG $(LIBS)

# --- CORRECTED Rules for version.o and version.cc ---
# `version.o` depends on `version.cc`.
version.o: version.cc
	$(CXX) -c $< -o $@ $(CXXFLAGS) $(INCLUDE_PATHS)

# Rule to create `version.cc` if it doesn't exist.
# `make` will run this rule automatically when it sees `version.o` needs `version.cc`.
version.cc:
	@echo "Creating dummy version file: version.cc"
	@echo '#include <string>' > version.cc
	@echo 'namespace version {' >> version.cc
	@echo '  std::string BuildVersion() { return "user-build"; }' >> version.cc
	@echo '}' >> version.cc

# --- Generic Rules for Compiling C++ Source Files ---
%.o: %.cc %.hh
	$(CXX) -c $< -o $@ $(CXXFLAGS) $(INCLUDE_PATHS)

%.o: %.cc
	$(CXX) -c $< -o $@ $(CXXFLAGS) $(INCLUDE_PATHS)

$(BOOST_SRC_DIR)/%.o: $(BOOST_SRC_DIR)/%.cpp
	$(CXX) -c $< -o $@ $(CXXFLAGS) $(INCLUDE_PATHS)

# =========================================================================
# Utility Commands
# =========================================================================

clean:
	@echo "Cleaning up object files and targets..."
	rm -f *.o *.so $(TARGET_EXE) $(BOOST_SRC_DIR)/*.o version.cc ./../usr/lib/* ./../usr/include/* ./../usr/bin/*

# (install and splashscreen rules remain the same)
install: all splashscreen
	@echo "Installing to $(INSTDIR)..."
	@mkdir -p $(INSTDIR)/lib $(INSTDIR)/include $(INSTDIR)/bin
	@ln -sf $(PWD)/$(TARGET_LIB) $(INSTDIR)/lib/$(TARGET_LIB)
	@for header in *.hh; do \
		ln -sf $(PWD)/$$header $(INSTDIR)/include/$$header; \
	done
	@ln -sf $(PWD)/armadillo $(INSTDIR)/include/armadillo
	@ln -sf $(PWD)/$(TARGET_EXE) $(INSTDIR)/bin/$(TARGET_EXE)
	@printf "\n\nInstallation complete.\n\n"
	@echo '*********************************************************************'
	@echo '* Make sure $(INSTDIR)/lib is in your LD_LIBRARY_PATH (Linux) *'
	@echo '* or DYLD_LIBRARY_PATH (macOS).                                   *'
	@echo '* Also, ensure $(INSTDIR)/bin is in your PATH.                    *'
	@echo '*********************************************************************'

splashscreen:
	@printf "\n"
	@printf "                                                      ____                                     \n"
	@printf "            _________________           _____________/   /\               _________________    \n"
	@printf "           /____/_____/_____/|         /____/_____/ /___/  \             /____/_____/_____/|   \n"
	@printf "          /____/_____/__G_ /||        /____/_____/|/   /\  /\           /____/_____/____ /||   \n"
	@printf "         /____/_____/__+__/|||       /____/_____/|/ G /  \/  \         /____/_____/_____/|||   \n"
	@printf "        |     |     |     ||||      |     |     |/___/   /\  /\       |     |     |     ||||   \n"
	@printf "        |  I  |  M  |     ||/|      |  I  |  M  /   /\  /  \/  \      |  I  |  M  |     ||/|   \n"
	@printf "        |_____|_____|_____|/||      |_____|____/ + /  \/   /\  /      |_____|_____|_____|/||   \n"
	@printf "        |     |     |     ||||      |     |   / __/   /\  /  \/       |     |     |     ||||   \n"
	@printf "        |  S  |  R  |     ||/|      |  S  |   \   \  /  \/   /        |  S  |  R  |  G  ||/|   \n"
	@printf "        |_____|_____|_____|/||      |_____|____\ __\/   /\  /         |_____|_____|_____|/||   \n"
	@printf "        |     |     |     ||||      |     |     \   \  /  \/          |     |     |     ||||   \n"
	@printf "        |     |  +  |     ||/       |     |  +  |\ __\/   /           |     |  +  |  +  ||/    \n"
	@printf "        |_____|_____|_____|/        |_____|_____|/\   \  /            |_____|_____|_____|/     \n"
	@printf "                                                   \___\/                                      \n"
	@printf "\n"