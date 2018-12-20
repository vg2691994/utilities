
import numpy as N

def save_to_dada(data, out_name, header_size = 16384, telescope = "MOST", source="FAKE", freq = 835.5957031, bw = -31.25, npol = 1, nbit = 32, tsamp = 0.00032768, utc_start = "2018-02-12-00:00:00", order = "TF", dm = 0.0):
  
  
  '''
  Saves a numpy.ndarray to a dada file on disk

  ---------------------
  Input:
  data:   numpy.ndarray
          The array which contains the data to be written
          Can be 1d or 2d

  out_name: str
            Name of the output file.
            Can contain the full absolute path

  ----------------------
  Optional params:
  header_size:  int
                Size of the header in bytes
                Def: 16384

  telescope:    str
                Name of the telescope
                Def: MOST

  source:       str
                Name of the source
                Def: FAKE

  freq:         float
                Center frequency in MHz
                Def: 835.5957031
                
  bw:           float
                Bandwidth in MHz (can be positive or negative)
                Def: -31.25

  npol:         int
                Number of polarisations (Currently only data with npol = 1 is supported)
                Def :1

  nbit:         int
                nibts to use to save the data. Supported values:
                8 - Data will be casted into signed 8 bit integers
                16 - Data will be casted into signed 16 bit integers
                32 - Data will be casted into 32 bit floats
                Def: 32

  tsamp:        float
                Sampling time in seconds
                Def: 0.00032768

  utc_start:    str
                UTC_START
                Def: 2018-02-12:00:00:00

  order:        str
                The order to save data in. Supported values:
                TF- Time frequency order
                FT - Frequency time order
                Def: TF

  dm:           float
                Dispersion measure in pc cm-3
                Def: 0

  '''       

  if not type(data) == N.ndarray:
    raise "Only numpy ndarrays can be written out"
  if data.ndim ==1:
    nch =1
    nsamps = data.shape[0]
    order = "T"
  if data.ndim ==2:
    nch = data.shape[0]
    nsamps = data.shape[1]
  if data.ndim >2:
    raise "Cannot accept arrays with more than 2 dimensions, given array has {0} dimensions".format(data.ndim)

  if nbit == 8:
    data = data.astype('int8')
  elif nbit == 16:
    data = data.astype('int16')
  elif nbit == 32:
    data = data.astype('float32')
  else:
    raise "{0} nbit is unkown. Only 8 (int), 16 (int) and 32 (float) are supported".format(nbit)

  if npol != 1:
    raise "Only npol = 1 is supported currently"

  if order == "TF":
    O = 'F'
  elif order == "FT":
    O = 'C'
  elif order == "T":
    O = 'F'
  else:
    raise "Only FT and TF orders are understood. Given: {0}".format(order)
  
  params = {
           "HDR_VERSION":  1.0,
            "HDR_SIZE": header_size,
            "TELESCOPE":    telescope,
            "SOURCE":   source,
            "FREQ": freq,         
            "BW":   bw,          
            "NPOL": npol,
            "NBIT": nbit,
            "TSAMP":    tsamp * 1e6,            #usec   --Dont change this, dspsr needs tsamp in microseconds to work properly
            "NSAMPS":   nsamps,
            "UTC_START":   utc_start, 
            "STATE":    "Intensity",
            "OBS_OFFSET":   0,           
            "NCHAN":    nch,
            "NDIM":     1, 
            "ORDER":    order,            #This is ensured later in the code while writing data with flatten(order=O)
            "INSTRUMENT":   "MOPSR",
            "DM":   dm, 
            }

  header = ""
  for i in params:
    header += i
    tabs = 3 - int(len(i)/8)
    header += "\t"*tabs
    header += str(params[i]) + "\n"
  leftover_space = header_size - len(header)
  header += '\0' * leftover_space

  out = open(out_name, 'wb')
  out.write(header)

  data.flatten(order = O).tofile(out)

  out.close()

  print "Succesfully written data to {0}".format(out_name)
  return 0


