# Makefile to compile predator for Pursuit program
# Date: 15-3-2002
# Author: Jelle Kok
# Usage: make (or gmake on Solaris) will create predator
#        for linux set correct OSFLAG and CFLAGS_LIBS.

CC                      = g++ 
COMPILE                 = $(CC) $(INCLUDES) ${FLAGS} ${DEFINES}

SRC_DIR                 = .
DST_DIR                 = .
TARGET                  = predator 

# Just uncomment Solaris to compile it under Solaris
# SOLARIS                 = 1

ifdef SOLARIS
INCLUDES	        = ${INCLUDES_SunOS_5}
OSFLAGS                 = $(OSFLAGS_SunOS_5)
CFLAGS_LIBS             = ${CLIBS_SunOS_5}
OBJECT_LIB              = ${OBJECT_LIB_SunOS_5}
else
INCLUDES	              = ${INCLUDES_linux}
OSFLAGS                 = ${OSFLAGS_linux} 
CFLAGS_LIBS             = ${CLIBS_linux}
OBJECT_LIB              = ${OBJECT_LIB_linux}
endif

# ==== INCLUDES =================================================

INCLUDES_linux          = #-I/home/stud/mas/include 
INCLUDES_SunOS_5        = #-I/home/stud/mas/include 

# ==== FLAGS ====================================================

#CFLAGS_DEBUG            = -pg -g
CFLAGS_OPT              = -O3 
CFLAGS_WARN             = -Wall

OSFLAGS_SunOS_5         = -DSolaris 
OSFLAGS_linux           = -Dlinux 

FLAGS                   = ${OSFLAGS} ${CFLAGS_OPT} ${CFLAGS_DEBUG} ${CFLAGS_WARN}

# ==== INCLUDED OBJECT LIBRARIES =================================

OBJECT_LIB_linux        = #/home/stud/mas/lib/Connection.o
OBJECT_LIB_SunOS_5      = #/home/stud/mas/lib/Connection.o

# ==== LIBS ====================================================

CLIBS_SunOS_5           =  -lsocket -lnsl -lpthread #-L/home/stud/mas/lib
CLIBS_linux             = 

# ==== DEFINES =================================================

DEFINES	                = 

# ==== SOURCES =================================================

SRCS		=	\
		Predator.C \
		Connection.C
		
OBJS   	= $(SRCS:.C=.o) 

# ==== RULES ==================================================

all::	$(TARGET)

.C.o:
	$(COMPILE) -c -o $@ $(@F:%.o=%.C)


predator: $(OBJS)  
	$(COMPILE) -o  $@ $(OBJS) ${OBJECT_LIB} ${CFLAGS_LIBS}
	
clean:
	rm -f $(TARGET) $(OBJS) *core a.out

depend:
	makedepend $(DEPENDFLAGS) -s "# DO NOT DELETE THIS LINE" -- $(INCLUDES) -- $(SRCS)

# DO NOT DELETE THIS LINE
