import os
import argparse
import uproot
import mplhep
import mpl_scatter_density # adds projection='scatter_density'
import matplotlib.pyplot as plt
import matplotlib.colors as colors
from matplotlib.ticker import AutoMinorLocator, MultipleLocator, FixedLocator
import copy
import numpy as np
import yaml

import matplotlib
# For serif font:
matplotlib.rcParams['font.family'] = 'serif'
matplotlib.rcParams['font.serif'] = 'Times New Roman'
#matplotlib.rcParams['agg.path.chunksize'] = 10000
#matplotlib.rcParams['figure.constrained_layout.use'] = True
color_cycle = matplotlib.rcParams['axes.prop_cycle'].by_key()['color'] # access the color cycle
LZcolors = { 
  'black' : 'black', 
  'blue' : color_cycle[0],
  'orange' : color_cycle[1],
  'green' : color_cycle[2],
  'red' : color_cycle[3],
  'purple' : color_cycle[4],
  'brown' : color_cycle[5],
  'magenta' : color_cycle[6],
  'grey' : color_cycle[7],
  'yellow' : color_cycle[8],
  'cyan' : color_cycle[9]
}


#______________________________________________________________________________
def argsetup():

  argparser = argparse.ArgumentParser(description="Generate SR1 WS plots")
  argparser.add_argument('-i', '--infile',
    help='Input histogram file')
  argparser.add_argument('-o', '--outfolder',
    help='Output directory of saved figures')
  argparser.add_argument('-p', '--params',
    help='YAML parameters file')
  return argparser.parse_args()

#______________________________________________________________________________
def read_params(param_file):
  with open (param_file, 'r') as stream:
    try:
      return yaml.safe_load(stream)
    except yaml.YAMLError as exc:
      print(exc)


class FigMaker:

  def __init__(self, params, in_hist_file=None, out_folder=None):
    self.params = params 
    if in_hist_file is not None:
      self.in_hist_file = in_hist_file
    else:
      self.in_hist_file = self.params['hist_file']
    if out_folder is not None:
      self.out_folder = out_folder 
    else:
      self.out_folder = self.params['output_folder']

    self.colors = {
      'pass' : LZcolors['black'],
      'fail' : LZcolors['orange'],
      'skin_tagged' : LZcolors['cyan'],
      'od_tagged' : LZcolors['purple'],
      'ER_band' : LZcolors['blue'],
      'NR_band' : LZcolors['red'],
      'FV' : LZcolors['green'],
      'AV' : LZcolors['yellow'],
      's2thr' : LZcolors['green']
    }
    
    os.makedirs(self.out_folder,exist_ok=True)



  #______________________________________________________________________________
  # Energy contours
  def make_energy_contours(self, energies, recoil_type='ER', logx = False, logy = True):
    '''
    Generate array data representing energy contours, given an input list of energies and recoil type 
    '''
    W = self.params['W']
    g1 = self.params['g1']
    g2 = self.params['g2']
    alpha = self.params['alpha'] 
    beta = self.params['beta']
    result = {}
    for energy in energies:
      # E = W * (S1/g1 + S2/g2)
      #W = 13.5e-3
      if logx:
        S1vals = np.linspace(0,5,1000)
        S1valsToUse = np.power(10., S1vals)
      else:
        S1vals = np.linspace(0.1,800,1000)
        S1valsToUse = S1vals
      if recoil_type == 'NR':
        S2vals = (alpha * np.power(energy, beta) - S1valsToUse / g1)*g2
      else:
        S2vals = (energy / W - S1valsToUse/g1) * g2 
          
      if logy:
        S2vals[S2vals<=0] = 1e-9
        S2vals = np.log10(S2vals)
        S2vals[S2vals<2] = -999
      result[energy] = (S1vals, S2vals)
    return result

  def plot_energy_contours(self, ax, Evals, recoil_type = 'ER', logy = True, logx=False, color='gray', lw=0.3, cutoff=200, ypos=2, rotation=-90):
    '''
    Overlay energy contours on an existing axes object 
    '''
    weight = 0.3
    contours = self.make_energy_contours(Evals, recoil_type = recoil_type, logy=logy, logx=logx)
    vals = np.array(list(contours.values()))
    xvals = np.transpose(vals[:,0])
    yvals = np.transpose(vals[:,1])
    ax.plot(xvals, yvals, color=color, lw=weight, zorder=5 )

    for energy, line in contours.items():
      xx = line[0]
      yy = line[1]
      xpos = xx[yy<2][2] # choose 2 points to the right to give some whitespace
      if xpos < cutoff:
        if recoil_type == 'NR':
          label = '{} keV$_{{nr}}$'.format(energy)
        else:
          label = '{} keV$_{{ee}}$'.format(energy)
        ax.text(xpos, ypos, label, rotation=rotation, rotation_mode='anchor', transform_rotates_text=True, color=color, fontsize='small')

  #______________________________________________________________________________
  # ER/NR band functions 
  def retrieve_band(self, band_file_name):
    '''
    Extract arrays representing an ER or NR band from a text file 
    '''
    data = []
    with open(band_file_name,'r') as f:
      counter = 0
      for line in f:
        # skip first line 
        if counter == 0:
          counter += 1
          continue
        row = line.rstrip().replace('\t', ' ').replace('[', '').replace(']','').split()
        #print(row)
        vals = [ float(i) for i in row ]
        data.append(vals)
        counter += 1
    data = np.transpose(data)
    res = {}
    res['S1'] = data[0]
    res['logS2mean'] = data[1]
    res['logS2upper'] = data[1] + data[2]
    res['logS2lower'] = data[1] - data[3]
    return res

  def retrieve_ER_band(self):
    ER_band_file = self.params['ER_band_file'] 
    return self.retrieve_band(ER_band_file)

  def retrieve_NR_band(self):
    NR_band_file = self.params['NR_band_file'] 
    return self.retrieve_band(NR_band_file)

  def plot_ER_band(self, ax, logx = False, color=None, lw=0.5):
    '''
    Overlay ER band on an existing axes object 
    '''
    band = self.retrieve_ER_band()

    if not color:
      color = self.colors['ER_band']

    if not logx:
      ax.plot(band['S1'], band['logS2mean'], color=color, lw=lw, zorder=20)
      ax.plot(band['S1'], band['logS2upper'], color=color, lw=lw, ls='--', zorder=20)
      ax.plot(band['S1'], band['logS2lower'], color=color, lw=lw, ls='--', zorder=20)
    else:
      ax.plot(np.log10(band['S1']), band['logS2mean'], color=color, lw=lw, zorder=20)
      ax.plot(np.log10(band['S1']), band['logS2upper'], color=color, lw=lw, ls='--', zorder=20)
      ax.plot(np.log10(band['S1']), band['logS2lower'], color=color, lw=lw, ls='--', zorder=20)

  def plot_NR_band(self, ax, logx = False, color=None, lw=0.5):
    '''
    Overlay NR band on an existing axes object 
    '''
    band = self.retrieve_NR_band()

    if not color:
      color = self.colors['NR_band']

    if not logx:
      ax.plot(band['S1'], band['logS2mean'], color=color, lw=lw, zorder=20)
      ax.plot(band['S1'], band['logS2upper'], color=color, lw=lw, ls='--', zorder=20)
      ax.plot(band['S1'], band['logS2lower'], color=color, lw=lw, ls='--', zorder=20)
    else:
      ax.plot(np.log10(band['S1']), band['logS2mean'], color=color, lw=lw, zorder=20)
      ax.plot(np.log10(band['S1']), band['logS2upper'], color=color, lw=lw, ls='--', zorder=20)
      ax.plot(np.log10(band['S1']), band['logS2lower'], color=color, lw=lw, ls='--', zorder=20)



  #______________________________________________________________________________
  # FV functions 
  def FVr(self, drift, standoff=4):
    '''
    Function to return FV radius, given a drift time and standoff distance 
    '''
    pol = [72.4403, 0.00933984, 5.06325e-5, 1.65361e-7, 2.92605e-10, 2.53539e-13, 8.30075e-17] # updated wall def from Nishat
    result = np.zeros_like(drift)
    for i in range(len(pol)):
      result = result + pol[i]*np.power(-drift, i)
    
    try:
      iterator = iter(result)
    except TypeError:
      result -= standoff 
    else:
      for i in range(len(drift)):
        if drift[i] < 200.:
          result[i] = result[i] - 5.2 
        elif drift[i] > 800 :
          result[i] = result[i] - 5.0
        else:
          result[i] = result[i] - standoff
    return result
      

  def plot_FV(self, ax, standoff=4, color=None, lw=0.5):
    '''
    Overlay FV definition on an existing axes object 
    '''
    FVz_upper = self.params['FVz_upper'] 
    FVz_lower = self.params['FVz_lower'] 
    dt_min = FVz_upper
    dt_max = FVz_lower
    dt_vals = np.arange(dt_min, dt_max, 1)
    r_vals = self.FVr(dt_vals, standoff=standoff)
    FV_wall_dt = dt_vals
    FV_wall_r = r_vals #- standoff # FV is fixed standoff distance from AV wall
    FV_top_r = np.arange(0, FV_wall_r[0], 0.1)
    FV_top_dt = np.zeros(len(FV_top_r)) + dt_min
    FV_bot_r = np.arange(0, FV_wall_r[-1], 0.1)
    FV_bot_dt = np.zeros(len(FV_bot_r)) + dt_max

    if not color:
      color = self.colors['FV']

    ax.plot(FV_top_r**2, -FV_top_dt, color=color, lw=lw, ls='--', zorder=20)
    ax.plot(FV_bot_r**2, -FV_bot_dt, color=color, lw=lw, ls='--', zorder=20)
    ax.plot(FV_wall_r**2, -FV_wall_dt, color=color, lw=lw, ls='--', zorder=20)

  def plot_xy_FV(self, ax, standoff=4, color=None, lw=0.5):
    '''
    Overlay FV radius on xy plot.
    Include two radii: top and bottom of FV. 
    '''

    FVz_upper = self.params['FVz_upper'] 
    FVz_lower = self.params['FVz_lower'] 
    dt_min = FVz_upper
    dt_max = FVz_lower

    FVr_upper = self.FVr(dt_min, standoff=standoff)
    FVr_lower = self.FVr(dt_max, standoff=standoff)

    npts = 1000
    circle_theta = np.linspace(0,2.*np.pi, npts)
    circle_xvals = np.sin(circle_theta)
    circle_yvals = np.cos(circle_theta)
    FVr_upper_xvals = FVr_upper * circle_xvals
    FVr_upper_yvals = FVr_upper * circle_yvals
    FVr_lower_xvals = FVr_lower * circle_xvals
    FVr_lower_yvals = FVr_lower * circle_yvals

    if not color:
      color = self.colors['FV']
    
    ax.plot(FVr_upper_xvals, FVr_upper_yvals, color=color, lw=lw, ls='-', zorder=20)
    ax.plot(FVr_lower_xvals, FVr_lower_yvals, color=color, lw=lw, ls='--', zorder=20)

  #______________________________________________________________________________
  # Histogram plotting functions 
  def plot_cut_set(self, file, hist, cut_name, cIdx, hIdx, invertedCut = False, folder='figures', save_fig=False):
    
    fig, axs = plt.subplots(2,2, figsize=(12,10))
    axs = axs.flatten()
      
    if not invertedCut:
      pass_cut_name = cut_name 
      fail_cut_name = '!' + cut_name
    else:
      pass_cut_name = '!' + cut_name 
      fail_cut_name = cut_name
    
    h_pass_all = 'h_{hIdx:04d}_{cx}_{hist}'.format(hIdx=hIdx,      cx=pass_cut_name, hist=hist)
    h_pass_LE =  'h_{hIdx:04d}_{cx}_{hist}'.format(hIdx=hIdx+1000, cx=pass_cut_name+'_LE', hist=hist)
    h_fail_all = 'h_{hIdx:04d}_{cx}_{hist}'.format(hIdx=hIdx+50,   cx=fail_cut_name, hist=hist)
    h_fail_LE =  'h_{hIdx:04d}_{cx}_{hist}'.format(hIdx=hIdx+1050, cx=fail_cut_name+'_LE', hist=hist)
    
    # plotter barfs if try to plot an empty histogram with log colorscale. so check for nonempty before plotting.
    cut_folder = 'CX{cIdx:02d}_{cx}'.format(cIdx=cIdx, cx=cut_name)
    h = file['WS'][cut_folder][h_pass_all].to_hist()
    if np.sum(h.counts()) >= 1:
      h.plot(ax=axs[0], cmin=0.1, norm=colors.LogNorm(), zorder=10)
    h = file['WS'][cut_folder][h_pass_LE].to_hist()
    if np.sum(h.counts()) >= 1:
      h.plot(ax=axs[1], cmin=0.1, zorder=10)
    h = file['WS'][cut_folder][h_fail_all].to_hist()
    if np.sum(h.counts()) >= 1:
      h.plot(ax=axs[2], cmin=0.1, norm=colors.LogNorm(), zorder=10)
    h = file['WS'][cut_folder][h_fail_LE].to_hist()
    if np.sum(h.counts()) >= 1:
      h.plot(ax=axs[3], cmin=0.1, zorder=10)
    
    # set plot titles
    axs[0].set_title(pass_cut_name)
    axs[1].set_title(pass_cut_name+'_LE')
    axs[2].set_title(fail_cut_name)
    axs[3].set_title(fail_cut_name+'_LE')
    
    for ax in axs:
      ax.set_axisbelow(True)
      ax.grid('both',color='lightgray')
      ax.xaxis.set_minor_locator(AutoMinorLocator())
      ax.yaxis.set_minor_locator(AutoMinorLocator())
      
    # plot energy contours. only for cS2/cS1 plot 
    if hist == 'cS2_cS1':

      LEcontours = [1,3,5,10,20,30,40]
      recoil_type = 'ER'
      self.plot_energy_contours(axs[1], LEcontours, recoil_type=recoil_type, logx=False, logy=True, cutoff=200)
      self.plot_energy_contours(axs[3], LEcontours, recoil_type=recoil_type, logx=False, logy=True, cutoff=200)
      self.plot_ER_band(axs[1], logx=False)
      self.plot_ER_band(axs[3], logx=False)
      self.plot_NR_band(axs[1], logx=False)
      self.plot_NR_band(axs[3], logx=False)
      
      #contours = make_Eee_contours([1,2,10,20,100,200, 1000], g1, g2, logx=True, logy=True)
      HEcontours = [1,3,6,10,30,60, 100,300,600, 1000]
      self.plot_energy_contours(axs[0], HEcontours, recoil_type=recoil_type, logx=True, logy=True, cutoff=4)
      self.plot_energy_contours(axs[2], HEcontours, recoil_type=recoil_type, logx=True, logy=True, cutoff=4)
      self.plot_ER_band(axs[0], logx=True)
      self.plot_ER_band(axs[2], logx=True)
      self.plot_NR_band(axs[0], logx=True)
      self.plot_NR_band(axs[2], logx=True)
        
      S2thr_lower = self.params['S2thr_lower'] 
      S2thr_upper = self.params['S2thr_upper'] 
      for ax in axs:
        ax.plot([0,200],[S2thr_lower, S2thr_lower],ls='--', lw=0.5, color=self.colors['s2thr'])
        ax.plot([0,200],[S2thr_upper, S2thr_upper],ls='--', lw=0.5, color=self.colors['s2thr'])

        

    if hist == 'dt_r':
      for ax in axs:
        self.plot_FV(ax)    
    
    fig.subplots_adjust(wspace=0.3, hspace=0.3, left=0.1, right=0.92, top=0.92, bottom=0.1)
    
    if save_fig:
      file_name = '{folder}/h_{hist}_{cIdx:02d}_{cx}.png'.format(folder=folder, hist=hist, cIdx=cIdx, cx=cut_name)
      print('Saving {} ...'.format(file_name))
      fig.savefig(file_name, dpi=300, facecolor='white')

    plt.close(fig)

  #______________________________________________________________________________
  # Plot all histograms for a given cut 
  def plot_hist_set(self, file, cut_name, cIdx, **kwargs):
    '''
    Generate plots for (pass, fail) + (fullE, lowE) for each parameter space, all for the same cut.
    '''    
    self.plot_cut_set(file, 's2_s1', cut_name, cIdx, 0, **kwargs)
    self.plot_cut_set(file, 'cS2_cS1', cut_name, cIdx, 1, **kwargs)
    self.plot_cut_set(file, 'dt_r', cut_name, cIdx, 2, **kwargs)
    self.plot_cut_set(file, 'xy', cut_name, cIdx, 3, **kwargs)
    self.plot_cut_set(file, 's1_dt', cut_name, cIdx, 4, **kwargs)
    self.plot_cut_set(file, 's2_dt', cut_name, cIdx, 5, **kwargs)
    self.plot_cut_set(file, 's1_r', cut_name, cIdx, 6, **kwargs)
    self.plot_cut_set(file, 's2_r', cut_name, cIdx, 7, **kwargs)


  #______________________________________________________________________________
  # Generate all the plots for all the cuts 
  def plot_all_cuts(self, save_fig=False):

    in_hist_file = self.in_hist_file 
    out_folder = self.out_folder 
    cutlist = self.params['cut_list']

    print('Opening {}'.format(in_hist_file))
    file = uproot.open(in_hist_file)

    os.makedirs(out_folder, exist_ok=True)

    # for >=v18
    # self.plot_hist_set(file, 'SS', 1,        folder=out_folder, save_fig=save_fig)
    # self.plot_hist_set(file, 'HSX', 2,       folder=out_folder, save_fig=save_fig)
    # self.plot_hist_set(file, 'MUONVETO', 3,  folder=out_folder, save_fig=save_fig)
    # self.plot_hist_set(file, 'ETV', 4,       folder=out_folder, save_fig=save_fig)
    # self.plot_hist_set(file, 'BUFFERS', 5,   folder=out_folder, save_fig=save_fig)
    # self.plot_hist_set(file, 'SSWINDOW', 6,  folder=out_folder, save_fig=save_fig)
    # self.plot_hist_set(file, 'XYQUAL', 7,    folder=out_folder, save_fig=save_fig)
    # self.plot_hist_set(file, 'ABOVEANODE', 8,folder=out_folder, save_fig=save_fig)
    # self.plot_hist_set(file, 'GATE', 9,      folder=out_folder, save_fig=save_fig)
    # self.plot_hist_set(file, 'CATH', 10,     folder=out_folder, save_fig=save_fig)
    # self.plot_hist_set(file, 'FCRES', 11,    folder=out_folder, save_fig=save_fig)
    # self.plot_hist_set(file, 'S2WIDTH', 12,  folder=out_folder, save_fig=save_fig)
    # self.plot_hist_set(file, 'S1TBA', 13,    folder=out_folder, save_fig=save_fig)
    # self.plot_hist_set(file, 'STINGER', 14,  folder=out_folder, save_fig=save_fig)
    # self.plot_hist_set(file, 'HSC', 15,      folder=out_folder, save_fig=save_fig)
    # self.plot_hist_set(file, 'EXCESSAREA',16,folder=out_folder, save_fig=save_fig)
    # self.plot_hist_set(file, 'HIGHRATE', 17, folder=out_folder, save_fig=save_fig)
    # self.plot_hist_set(file, 'S1RATE',   18, folder=out_folder, save_fig=save_fig)
    # self.plot_hist_set(file, 'S2THR',   19,  folder=out_folder, save_fig=save_fig)
    # self.plot_hist_set(file, 'ODV', 20,      folder=out_folder, save_fig=save_fig)
    # self.plot_hist_set(file, 'SKINV', 21,    folder=out_folder, save_fig=save_fig)

    counter = 1
    for cx in cutlist:
      self.plot_hist_set(file, cx, counter, folder=out_folder, save_fig=save_fig)
      counter += 1

    plt.close()

  #______________________________________________________________________________
  # Plot cS1 vs. logcS2 on an axes object 
  def plot_scatter(self, ax, cS1, logcS2, color='black', alpha=1, marker='.', markersize=2, fill=True, 
    minX=0, maxX=120, minY=1, maxY=6, 
    label='', xlabel='', ylabel=''):
    mec = color 
    mfc = color if fill else 'none'
    ax.plot(cS1, logcS2, ls='', marker=marker, color=color, alpha=alpha, markersize=markersize, label=label, mec=mec, mfc=mfc)
    # ax.fill_between([0,200],[5,5], [5.5, 5.5], color='none', edgecolor='magenta', hatch='/',ls='--')
    # ax.fill_between([0,200],[np.log10(52*5.5), np.log10(52*5.5)], [0,0], color='none', edgecolor='magenta', hatch='/',ls='--')

    ax.set_xlim(minX, maxX)
    ax.set_ylim(minY, maxY)
    ax.set_xlabel(xlabel) #'cS1 [phd]')
    ax.set_ylabel(ylabel) #'Log$_{10}$(cS2 [phd])')
    ax.xaxis.set_minor_locator(AutoMinorLocator())
    ax.yaxis.set_minor_locator(AutoMinorLocator())
    ax.grid('both',color='lightgray')

  #______________________________________________________________________________
  # Plot a uprooted TGraph onto an axes object, including energy contours 
  def plot_cS2cS1_scatter_formatted(self, ax, gr, **kwargs):
      
    # plot the points
    cS1 = gr.values(axis='x')
    logcS2 = gr.values(axis='y')
    self.plot_scatter(ax, cS1, logcS2, xlabel='cS1 [phd]',ylabel='Log$_{10}$(cS2 [phd])', **kwargs)
    
    # plot energy contours
    LE_ER_contours = [1,3,5,10,20,30]
    self.plot_energy_contours(ax, LE_ER_contours, recoil_type='ER', logx=False, logy=True, cutoff=120, ypos=1.8, rotation=-90, color='gray')
    
    # plot ER, NR bands
    self.plot_ER_band(ax, logx=False,color='blue')
    self.plot_NR_band(ax, logx=False,color='red')

    S2thr_upper = self.params['S2thr_upper'] 
    S2thr_lower = self.params['S2thr_lower'] 
    
    # plot S2 thresholds
    ax.plot([0,200],[S2thr_lower, S2thr_lower],ls='--', lw=0.5, color=self.colors['s2thr'])
    ax.plot([0,200],[S2thr_upper, S2thr_upper],ls='--', lw=0.5, color=self.colors['s2thr'])

  #______________________________________________________________________________
  # Plot a uproot r-drift TGraph onto axes 
  def plot_rdrift_scatter_formatted(self, ax, gr, **kwargs):

    # get the points 
    r2 = gr.values(axis='x')
    drift = gr.values(axis='y')
    
    # make the plot
    self.plot_scatter(ax, r2, drift, xlabel='r$^2$ [cm$^2$]', ylabel='-drift [us]', minX=0, maxX=80*80, minY=-1400, maxY=10, **kwargs)

    # plot the FV contour 
    self.plot_FV(ax)

  #______________________________________________________________________________
  # Project r-drift TGraph into drift and put on axes object
  def plot_drift_proj_formatted(self, ax, grs, minX=-10, maxX=1400, binsize=5, yscale='log', **kwargs):

    # get the points 
    # grs = multiple TGraphs.
    # concatenate into single array 
    drift = np.zeros(0)
    for gr in grs:
      drift = np.concatenate([drift, gr.values(axis='y')])
    drift = -drift 

    # define the bins 
    drift_bins = np.arange(minX,maxX, binsize)
    drift_hist = np.histogram(drift, drift_bins)
    mplhep.histplot(drift_hist, ax=ax, zorder=10, **kwargs)
    ax.set_xlim(minX, maxX)
    ax.set_yscale(yscale)
    ax.set_xlabel('drift [us]')
    ax.grid('both', zorder=0)

  #______________________________________________________________________________
  # Project r-drift TGraph into r2 and put on axes object
  def plot_r2_proj_formatted(self, ax, grs, minX=0, maxX=6400, binsize=50, yscale='log', **kwargs):

    # get the points 
    # grs = multiple TGraphs.
    # concatenate into single array
    r2 = np.zeros(0)
    for gr in grs:
      r2 = np.concatenate([r2, gr.values(axis='x')]) 
    
    # define the bins 
    r2_bins = np.arange(minX,maxX, binsize)
    r2_hist = np.histogram(r2, r2_bins)
    mplhep.histplot(r2_hist, ax=ax, zorder=10, **kwargs)
    ax.set_xlim(minX, maxX)
    ax.set_yscale(yscale)
    ax.set_xlabel('r$^2$ [cm$^2$]')
    ax.grid('both', zorder=0)
  
  #______________________________________________________________________________
  # Plot a uproot xy TGraph onto axes 
  def plot_xy_scatter_formatted(self, ax, gr, **kwargs):

    # get the points 
    x = gr.values(axis='x')
    y = gr.values(axis='y')

    # make the plot
    self.plot_scatter(ax, x, y, xlabel='x [cm]', ylabel='y [cm]', minX=-80, maxX=80, minY=-80, maxY=80, **kwargs)
    ax.xaxis.set_major_locator(MultipleLocator(25))
    ax.yaxis.set_major_locator(MultipleLocator(25))

    # plot the XY boundary
    self.plot_xy_FV(ax)


  #______________________________________________________________________________
  # Plot scatter plot matrix for S2 vs. S1 
  # upper left: all inside FV: passing, tagged by Skin, tagged by OD
  # upper right: failing, inside FV 
  # lower left: all FVr shell: passing, failing, tagged by Skin, tagged by OD 
  # lower right: all FVz shell: passing, failing, tagged by Skin, tagged by OD 
  def plot_cut_s2s1_scatter(self, fig, file, cut_name, cIdx, folder='figures', save_fig=False):
    
    # fig, axs = plt.subplots(2,2, figsize=(12,10))
    axs = fig.subplots(2,2)
    axs = axs.flatten()
    
    # # derive the the gr names
    # if not invertedCut:
    #   pass_cut_name = cut_name 
    #   fail_cut_name = '!' + cut_name
    # else:
    #   pass_cut_name = '!' + cut_name 
    #   fail_cut_name = cut_name
    
    pass_cut_name = cut_name
    fail_cut_name = '!'+cut_name

    hist = 'cS2_cS1'

    g_pass_LE_FV =          'g_{hIdx:04d}_{cx}_{hist}'.format(hIdx=1008, cx=pass_cut_name+'_LE_FV', hist=hist)
    g_fail_LE_FV =          'g_{hIdx:04d}_{cx}_{hist}'.format(hIdx=1058, cx=fail_cut_name+'_LE_FV', hist=hist)
    g_pass_LE_FV_nODV =     'g_{hIdx:04d}_{cx}_{hist}'.format(hIdx=1108, cx=pass_cut_name+'_LE_FV_!ODV', hist=hist)
    g_pass_LE_FV_nSKINV =   'g_{hIdx:04d}_{cx}_{hist}'.format(hIdx=1208, cx=pass_cut_name+'_LE_FV_!SKINV', hist=hist)
    g_pass_LE_nFVr =        'g_{hIdx:04d}_{cx}_{hist}'.format(hIdx=1011, cx=pass_cut_name+'_LE_!FVr', hist=hist)
    g_pass_LE_nFVz =        'g_{hIdx:04d}_{cx}_{hist}'.format(hIdx=1014, cx=pass_cut_name+'_LE_!FVz', hist=hist)
    g_fail_LE_nFVr =        'g_{hIdx:04d}_{cx}_{hist}'.format(hIdx=1061, cx=fail_cut_name+'_LE_!FVr', hist=hist)
    g_fail_LE_nFVz =        'g_{hIdx:04d}_{cx}_{hist}'.format(hIdx=1064, cx=fail_cut_name+'_LE_!FVz', hist=hist)
    g_pass_LE_nFVr_nODV =   'g_{hIdx:04d}_{cx}_{hist}'.format(hIdx=1111, cx=pass_cut_name+'_LE_!FVr_!ODV', hist=hist)
    g_pass_LE_nFVz_nODV =   'g_{hIdx:04d}_{cx}_{hist}'.format(hIdx=1114, cx=pass_cut_name+'_LE_!FVz_!ODV', hist=hist)
    g_pass_LE_nFVr_nSKINV = 'g_{hIdx:04d}_{cx}_{hist}'.format(hIdx=1211, cx=pass_cut_name+'_LE_!FVr_!SKINV', hist=hist)
    g_pass_LE_nFVz_nSKINV = 'g_{hIdx:04d}_{cx}_{hist}'.format(hIdx=1214, cx=pass_cut_name+'_LE_!FVz_!SKINV', hist=hist)

    cut_dir = 'CX{cIdx:02d}_{cx}'.format(cIdx=cIdx,cx=cut_name)

    # make the plots
    # upper left: passing, inside FV; failing, inside FV
    self.plot_cS2cS1_scatter_formatted(axs[0], file['WS'][cut_dir][g_pass_LE_FV], color=self.colors['pass'], label='pass')
    self.plot_cS2cS1_scatter_formatted(axs[0], file['WS'][cut_dir][g_pass_LE_FV_nSKINV], color=self.colors['skin_tagged'], label='Skin tagged')
    self.plot_cS2cS1_scatter_formatted(axs[0], file['WS'][cut_dir][g_pass_LE_FV_nODV], color=self.colors['od_tagged'], label='OD tagged')

    # upper right: passing, tagged by Skin; passing, tagged by OD 
    self.plot_cS2cS1_scatter_formatted(axs[1], file['WS'][cut_dir][g_fail_LE_FV], color=self.colors['fail'], label='fail')

    # lower left: all FVr shell: passing, failing, tagged by Skin, tagged by OD 
    self.plot_cS2cS1_scatter_formatted(axs[2], file['WS'][cut_dir][g_pass_LE_nFVr], color=self.colors['pass'], label='pass')
    self.plot_cS2cS1_scatter_formatted(axs[2], file['WS'][cut_dir][g_fail_LE_nFVr], color=self.colors['fail'], label='fail')
    self.plot_cS2cS1_scatter_formatted(axs[2], file['WS'][cut_dir][g_pass_LE_nFVr_nSKINV], color=self.colors['skin_tagged'] , label='Skin tagged')
    self.plot_cS2cS1_scatter_formatted(axs[2], file['WS'][cut_dir][g_pass_LE_nFVr_nODV], color=self.colors['od_tagged'], label='OD tagged')

    # lower right: all FVz shell: passing, failing, tagged by Skin, tagged by OD 
    self.plot_cS2cS1_scatter_formatted(axs[3], file['WS'][cut_dir][g_pass_LE_nFVz], color=self.colors['pass'], label='pass')
    self.plot_cS2cS1_scatter_formatted(axs[3], file['WS'][cut_dir][g_fail_LE_nFVz], color=self.colors['fail'], label='fail')
    self.plot_cS2cS1_scatter_formatted(axs[3], file['WS'][cut_dir][g_pass_LE_nFVz_nSKINV], color=self.colors['skin_tagged'] , label='Skin tagged')
    self.plot_cS2cS1_scatter_formatted(axs[3], file['WS'][cut_dir][g_pass_LE_nFVz_nODV], color=self.colors['od_tagged'], label='OD tagged')


    axs[0].set_title('{} - PASS - FV'.format(cut_dir))
    axs[1].set_title('{} - FAIL - FV'.format(cut_dir))
    axs[2].set_title('{} - !FVr'.format(cut_dir))
    axs[3].set_title('{} - !FVz'.format(cut_dir))
    
    
    # fig.subplots_adjust(wspace=0.3, hspace=0.3, left=0.1, right=0.92, top=0.92, bottom=0.1)
    
    # save fig
    # if (save_fig):
    #   file_name = '{folder}/g_{hist}_{cIdx:02d}_{cx}.png'.format(folder=folder, hist=hist, cIdx=cIdx, cx=cut_name)
    #   print('Saving {} ...'.format(file_name))
    #   fig.savefig(file_name, dpi=300, facecolor='white')
    
    # plt.close(fig)

  #______________________________________________________________________________
  # Plot scatter plot matrix for RZ
  # upper left: passing, tagged by Skin, tagged by OD
  # upper right: failing
  # lower left: drift projection, full AV vs. FVr 
  # lower right: r2 projection, full AV vs. FVz
  def plot_cut_rdrift_scatter(self, fig, file, cut_name, cIdx, folder='figures', save_fig=False):
    
    #fig, axs = plt.subplots(2,2, figsize=(12,10))
    axs = fig.subplots(2,2)
    axs = axs.flatten()

    pass_cut_name = cut_name
    fail_cut_name = '!'+cut_name

    hist = 'dt_r'

    g_pass_LE_FV =          'g_{hIdx:04d}_{cx}_{hist}'.format(hIdx=1009, cx=pass_cut_name+'_LE_FV', hist=hist)
    g_fail_LE_FV =          'g_{hIdx:04d}_{cx}_{hist}'.format(hIdx=1059, cx=fail_cut_name+'_LE_FV', hist=hist)
    g_pass_LE_FV_nODV =     'g_{hIdx:04d}_{cx}_{hist}'.format(hIdx=1109, cx=pass_cut_name+'_LE_FV_!ODV', hist=hist)
    g_pass_LE_FV_nSKINV =   'g_{hIdx:04d}_{cx}_{hist}'.format(hIdx=1209, cx=pass_cut_name+'_LE_FV_!SKINV', hist=hist)
    g_pass_LE_nFVr =        'g_{hIdx:04d}_{cx}_{hist}'.format(hIdx=1012, cx=pass_cut_name+'_LE_!FVr', hist=hist)
    g_pass_LE_nFVz =        'g_{hIdx:04d}_{cx}_{hist}'.format(hIdx=1015, cx=pass_cut_name+'_LE_!FVz', hist=hist)
    g_fail_LE_nFVr =        'g_{hIdx:04d}_{cx}_{hist}'.format(hIdx=1062, cx=fail_cut_name+'_LE_!FVr', hist=hist)
    g_fail_LE_nFVz =        'g_{hIdx:04d}_{cx}_{hist}'.format(hIdx=1065, cx=fail_cut_name+'_LE_!FVz', hist=hist)
    g_pass_LE_nFVr_nODV =   'g_{hIdx:04d}_{cx}_{hist}'.format(hIdx=1112, cx=pass_cut_name+'_LE_!FVr_!ODV', hist=hist)
    g_pass_LE_nFVz_nODV =   'g_{hIdx:04d}_{cx}_{hist}'.format(hIdx=1115, cx=pass_cut_name+'_LE_!FVz_!ODV', hist=hist)
    g_pass_LE_nFVr_nSKINV = 'g_{hIdx:04d}_{cx}_{hist}'.format(hIdx=1212, cx=pass_cut_name+'_LE_!FVr_!SKINV', hist=hist)
    g_pass_LE_nFVz_nSKINV = 'g_{hIdx:04d}_{cx}_{hist}'.format(hIdx=1215, cx=pass_cut_name+'_LE_!FVz_!SKINV', hist=hist)

    cut_dir = 'CX{cIdx:02d}_{cx}'.format(cIdx=cIdx,cx=cut_name)

    # make the plots
    # upper left: passing, tagged by Skin, tagged by OD
    self.plot_rdrift_scatter_formatted(axs[0], file['WS'][cut_dir][g_pass_LE_FV],   color=self.colors['pass'], label='pass')
    self.plot_rdrift_scatter_formatted(axs[0], file['WS'][cut_dir][g_pass_LE_nFVr], color=self.colors['pass'])
    self.plot_rdrift_scatter_formatted(axs[0], file['WS'][cut_dir][g_pass_LE_nFVz], color=self.colors['pass'])
    self.plot_rdrift_scatter_formatted(axs[0], file['WS'][cut_dir][g_pass_LE_FV_nSKINV],   color=self.colors['skin_tagged'] , marker='o', label='Skin tagged')
    self.plot_rdrift_scatter_formatted(axs[0], file['WS'][cut_dir][g_pass_LE_nFVr_nSKINV], color=self.colors['skin_tagged'] , marker='o')
    self.plot_rdrift_scatter_formatted(axs[0], file['WS'][cut_dir][g_pass_LE_nFVz_nSKINV], color=self.colors['skin_tagged'] , marker='o')
    self.plot_rdrift_scatter_formatted(axs[0], file['WS'][cut_dir][g_pass_LE_FV_nODV],   color=self.colors['od_tagged'], marker='o', label='OD tagged')
    self.plot_rdrift_scatter_formatted(axs[0], file['WS'][cut_dir][g_pass_LE_nFVr_nODV], color=self.colors['od_tagged'], marker='o')
    self.plot_rdrift_scatter_formatted(axs[0], file['WS'][cut_dir][g_pass_LE_nFVz_nODV], color=self.colors['od_tagged'], marker='o')


    # upper right: passing, tagged by Skin; passing, tagged by OD 
    self.plot_rdrift_scatter_formatted(axs[1], file['WS'][cut_dir][g_fail_LE_FV],   color=self.colors['fail'], label='fail')
    self.plot_rdrift_scatter_formatted(axs[1], file['WS'][cut_dir][g_fail_LE_nFVr], color=self.colors['fail'])
    self.plot_rdrift_scatter_formatted(axs[1], file['WS'][cut_dir][g_fail_LE_nFVz], color=self.colors['fail'])

    # lower left: drift time projection of upper left 
    grs = [ file['WS'][cut_dir][g_pass_LE_FV], file['WS'][cut_dir][g_pass_LE_nFVr], file['WS'][cut_dir][g_pass_LE_nFVz] ]
    self.plot_drift_proj_formatted(axs[2], grs, color=LZcolors['blue'])
    grs = [ file['WS'][cut_dir][g_pass_LE_FV] ]
    self.plot_drift_proj_formatted(axs[2], grs, color=LZcolors['black'])

    # lower right: r2 projection of upper left 
    grs = [ file['WS'][cut_dir][g_pass_LE_FV], file['WS'][cut_dir][g_pass_LE_nFVr], file['WS'][cut_dir][g_pass_LE_nFVz] ]
    self.plot_r2_proj_formatted(axs[3], grs, color=LZcolors['blue'])
    grs = [ file['WS'][cut_dir][g_pass_LE_FV], file['WS'][cut_dir][g_pass_LE_nFVr] ]
    self.plot_r2_proj_formatted(axs[3], grs, color=LZcolors['red'])
    grs = [ file['WS'][cut_dir][g_pass_LE_FV] ]
    self.plot_r2_proj_formatted(axs[3], grs, color=LZcolors['black'])

    axs[0].set_title('{} - PASS'.format(cut_dir))
    axs[1].set_title('{} - FAIL'.format(cut_dir))
    axs[2].set_title('{} - DRIFT'.format(cut_dir))
    axs[3].set_title('{} - R2'.format(cut_dir))
    
    
    # fig.subplots_adjust(wspace=0.3, hspace=0.3, left=0.1, right=0.92, top=0.92, bottom=0.1)
    
    # save fig
    # if (save_fig):
    #   file_name = '{folder}/g_{hist}_{cIdx:02d}_{cx}.png'.format(folder=folder, hist=hist, cIdx=cIdx, cx=cut_name)
    #   print('Saving {} ...'.format(file_name))
    #   fig.savefig(file_name, dpi=300, facecolor='white')

    # plt.close(fig)


#______________________________________________________________________________
  # Plot scatter plot matrix for XY
  def plot_cut_xy_scatter(self, fig, file, cut_name, cIdx, folder='figures', save_fig=False):
    
    #fig, axs = plt.subplots(2,2, figsize=(12,10))
    axs = fig.subplots(2,2)
    axs = axs.flatten()

    pass_cut_name = cut_name
    fail_cut_name = '!'+cut_name

    hist = 'xy'

    g_pass_LE_FV =          'g_{hIdx:04d}_{cx}_{hist}'.format(hIdx=1010, cx=pass_cut_name+'_LE_FV', hist=hist)
    g_fail_LE_FV =          'g_{hIdx:04d}_{cx}_{hist}'.format(hIdx=1060, cx=fail_cut_name+'_LE_FV', hist=hist)
    g_pass_LE_FV_nODV =     'g_{hIdx:04d}_{cx}_{hist}'.format(hIdx=1110, cx=pass_cut_name+'_LE_FV_!ODV', hist=hist)
    g_pass_LE_FV_nSKINV =   'g_{hIdx:04d}_{cx}_{hist}'.format(hIdx=1210, cx=pass_cut_name+'_LE_FV_!SKINV', hist=hist)
    g_pass_LE_nFVr =        'g_{hIdx:04d}_{cx}_{hist}'.format(hIdx=1013, cx=pass_cut_name+'_LE_!FVr', hist=hist)
    g_pass_LE_nFVz =        'g_{hIdx:04d}_{cx}_{hist}'.format(hIdx=1016, cx=pass_cut_name+'_LE_!FVz', hist=hist)
    g_fail_LE_nFVr =        'g_{hIdx:04d}_{cx}_{hist}'.format(hIdx=1063, cx=fail_cut_name+'_LE_!FVr', hist=hist)
    g_fail_LE_nFVz =        'g_{hIdx:04d}_{cx}_{hist}'.format(hIdx=1066, cx=fail_cut_name+'_LE_!FVz', hist=hist)
    g_pass_LE_nFVr_nODV =   'g_{hIdx:04d}_{cx}_{hist}'.format(hIdx=1113, cx=pass_cut_name+'_LE_!FVr_!ODV', hist=hist)
    g_pass_LE_nFVz_nODV =   'g_{hIdx:04d}_{cx}_{hist}'.format(hIdx=1116, cx=pass_cut_name+'_LE_!FVz_!ODV', hist=hist)
    g_pass_LE_nFVr_nSKINV = 'g_{hIdx:04d}_{cx}_{hist}'.format(hIdx=1213, cx=pass_cut_name+'_LE_!FVr_!SKINV', hist=hist)
    g_pass_LE_nFVz_nSKINV = 'g_{hIdx:04d}_{cx}_{hist}'.format(hIdx=1216, cx=pass_cut_name+'_LE_!FVz_!SKINV', hist=hist)

    cut_dir = 'CX{cIdx:02d}_{cx}'.format(cIdx=cIdx,cx=cut_name)

    # make the plots
    # upper left: passing, tagged by Skin, tagged by OD. show FV + !FVr, to not clutter top-down view 
    self.plot_xy_scatter_formatted(axs[0], file['WS'][cut_dir][g_pass_LE_FV],   color=self.colors['pass'], label='pass')
    self.plot_xy_scatter_formatted(axs[0], file['WS'][cut_dir][g_pass_LE_nFVr], color=self.colors['pass'])
    self.plot_xy_scatter_formatted(axs[0], file['WS'][cut_dir][g_pass_LE_FV_nSKINV],   color=self.colors['skin_tagged'] , marker='o', label='Skin tagged')
    self.plot_xy_scatter_formatted(axs[0], file['WS'][cut_dir][g_pass_LE_nFVr_nSKINV], color=self.colors['skin_tagged'] , marker='o')
    self.plot_xy_scatter_formatted(axs[0], file['WS'][cut_dir][g_pass_LE_FV_nODV],   color=self.colors['od_tagged'], marker='o', label='OD tagged')
    self.plot_xy_scatter_formatted(axs[0], file['WS'][cut_dir][g_pass_LE_nFVr_nODV], color=self.colors['od_tagged'], marker='o')

    # upper right: failing. show FV + !FVr
    self.plot_xy_scatter_formatted(axs[1], file['WS'][cut_dir][g_fail_LE_FV],   color=self.colors['fail'], label='fail')
    self.plot_xy_scatter_formatted(axs[1], file['WS'][cut_dir][g_fail_LE_nFVr], color=self.colors['fail'])

    # lower left: passing, tagged by Skin, tagged by OD, for !FVz
    self.plot_xy_scatter_formatted(axs[2], file['WS'][cut_dir][g_pass_LE_nFVz], color=self.colors['pass'])
    self.plot_xy_scatter_formatted(axs[2], file['WS'][cut_dir][g_pass_LE_nFVz_nSKINV], color=self.colors['skin_tagged'] , marker='o')
    self.plot_xy_scatter_formatted(axs[2], file['WS'][cut_dir][g_pass_LE_nFVz_nODV], color=self.colors['od_tagged'], marker='o')

    # lower right: failing, !FVz
    self.plot_xy_scatter_formatted(axs[3], file['WS'][cut_dir][g_fail_LE_nFVz], color=self.colors['fail'])


    axs[0].set_title('{} - PASS - FVz'.format(cut_dir))
    axs[1].set_title('{} - FAIL - FVz'.format(cut_dir))
    axs[2].set_title('{} - PASS - !FVz'.format(cut_dir))
    axs[3].set_title('{} - FAIL - !FVz'.format(cut_dir))
    
    
    # fig.subplots_adjust(wspace=0.3, hspace=0.3, left=0.1, right=0.92, top=0.92, bottom=0.1)
    
    # save fig
    # if (save_fig):
    #   file_name = '{folder}/g_{hist}_{cIdx:02d}_{cx}.png'.format(folder=folder, hist=hist, cIdx=cIdx, cx=cut_name)
    #   print('Saving {} ...'.format(file_name))
    #   fig.savefig(file_name, dpi=300, facecolor='white')

    # plt.close(fig)

  #______________________________________________________________________________
  # generate all scatter plots for given cut 
  def plot_scatter_set(self, file, cut_name, cIdx, folder, save_fig=False, **kwargs):
    fig = plt.figure(figsize=(24,20))
    subfigs = fig.subfigures(2, 2).flatten()
    self.plot_cut_s2s1_scatter(subfigs[0], file, cut_name, cIdx, **kwargs)
    self.plot_cut_rdrift_scatter(subfigs[2], file, cut_name, cIdx, **kwargs)
    self.plot_cut_xy_scatter(subfigs[3], file, cut_name, cIdx, **kwargs)
    
    fig.subplots_adjust(wspace=0.3, hspace=0.3, left=0.1, right=0.92, top=0.92, bottom=0.1)
    if (save_fig):
      file_name = '{folder}/g_{cIdx:02d}_{cx}.png'.format(folder=folder, cIdx=cIdx, cx=cut_name)
      fig.savefig(file_name, dpi=300, facecolor='white')
      print('Saved {}'.format(file_name))

    plt.close(fig)

  #______________________________________________________________________________
  # Make the plots! 
  # Generate all the plots for all the cuts 
  def plot_all_cuts_scatter(self, save_fig=False):
    
    in_hist_file = self.in_hist_file
    out_folder = self.out_folder 
    cutlist = self.params['cut_list']

    print('Opening {}'.format(in_hist_file))
    file = uproot.open(in_hist_file)

    os.makedirs(out_folder, exist_ok=True)

    # for >=v20
    # self.plot_scatter_set(file, 'HSX', 2,       folder=out_folder, save_fig=save_fig)
    # self.plot_scatter_set(file, 'MUONVETO', 3,  folder=out_folder, save_fig=save_fig)
    # self.plot_scatter_set(file, 'ETV', 4,       folder=out_folder, save_fig=save_fig)
    # self.plot_scatter_set(file, 'BUFFERS', 5,   folder=out_folder, save_fig=save_fig)
    # self.plot_scatter_set(file, 'SSWINDOW', 6,  folder=out_folder, save_fig=save_fig)
    # self.plot_scatter_set(file, 'XYQUAL', 7,    folder=out_folder, save_fig=save_fig)
    # self.plot_scatter_set(file, 'ABOVEANODE', 8,folder=out_folder, save_fig=save_fig)
    # self.plot_scatter_set(file, 'GATE', 9,      folder=out_folder, save_fig=save_fig)
    # self.plot_scatter_set(file, 'CATH', 10,     folder=out_folder, save_fig=save_fig)
    # self.plot_scatter_set(file, 'FCRES', 11,    folder=out_folder, save_fig=save_fig)
    # self.plot_scatter_set(file, 'S2WIDTH', 12,  folder=out_folder, save_fig=save_fig)
    # self.plot_scatter_set(file, 'S1TBA', 13,    folder=out_folder, save_fig=save_fig)
    # self.plot_scatter_set(file, 'STINGER', 14,  folder=out_folder, save_fig=save_fig)
    # self.plot_scatter_set(file, 'HSC', 15,      folder=out_folder, save_fig=save_fig)
    # self.plot_scatter_set(file, 'EXCESSAREA',16,folder=out_folder, save_fig=save_fig)
    # self.plot_scatter_set(file, 'HIGHRATE', 17, folder=out_folder, save_fig=save_fig)
    # self.plot_scatter_set(file, 'S1RATE',   18, folder=out_folder, save_fig=save_fig)
    # self.plot_scatter_set(file, 'S2THR',    19, folder=out_folder, save_fig=save_fig)
    # self.plot_scatter_set(file, 'ODV', 20,      folder=out_folder, save_fig=save_fig)
    # self.plot_scatter_set(file, 'SKINV', 21,    folder=out_folder, save_fig=save_fig)

    counter = 1
    for cx in cutlist:
      #print('cut: {}'.format(cx))
      self.plot_scatter_set(file, cx, counter, out_folder, save_fig=save_fig)
      counter += 1

    plt.close()

  #____________________________________________________________________________
  # Final WS datasets 
  def plot_WS_scatter(self, save_fig=False):
    
    in_hist_file = self.in_hist_file
    out_folder = self.out_folder 

    file = uproot.open(in_hist_file)

    fig, ax = plt.subplots(1,1)
    self.plot_cS2cS1_scatter_formatted(ax, file['WS']['g_WS_LE_cS2_cS1'], color='black')

    # save fig
    if (save_fig):
      file_name = '{folder}/g_WS_LE_cS2_cS1.png'.format(folder=out_folder)
      print('Saving {} ...'.format(file_name))
      fig.savefig(file_name, dpi=300, facecolor='white')

    # r-drift 
    fig, ax = plt.subplots(1,1)
    self.plot_rdrift_scatter_formatted(ax, file['WS']['g_WS_LE_dt_r'], color='black')
    if (save_fig):
      file_name = '{folder}/g_WS_LE_dt_r.png'.format(folder=out_folder)
      print('Saving {} ...'.format(file_name))
      fig.savefig(file_name, dpi=300, facecolor='white')

    # xy
    fig, axs = plt.subplots(1,3,figsize=(13,4))
    axs = axs.flatten()
    self.plot_xy_scatter_formatted(axs[0], file['WS']['g_WS_LE_AV_xy'], color='black', alpha=0.3, markersize=0.5)
    self.plot_xy_scatter_formatted(axs[1], file['WS']['g_WS_LE_FVz_xy'], color='black')
    self.plot_xy_scatter_formatted(axs[2], file['WS']['g_WS_LE_FV_xy'], color='black')
    fig.subplots_adjust(wspace=0.3, hspace=0.3, left=0.1, right=0.92, top=0.92, bottom=0.17)
    if (save_fig):
      file_name = '{folder}/g_WS_LE_xy.png'.format(folder=out_folder)
      print('Saving {} ...'.format(file_name))
      fig.savefig(file_name, dpi=300, facecolor='white')


    plt.close(fig)



def main():
  
  plt.style.use('./LZStyle/SetLZStyle.mplstyle')


  args = argsetup()
  
  hist_file = args.infile 
  out_folder = args.outfolder 
  params = read_params(args.params)

  figmaker = FigMaker(params, in_hist_file = hist_file , out_folder = out_folder)
  
  print('Input file: {}'.format(figmaker.in_hist_file))
  print('Output folder: {}'.format(figmaker.out_folder))

  # cut_list = params['cut_list']

  #figmaker.plot_all_cuts(save_fig = True)
  figmaker.plot_all_cuts_scatter(save_fig=True)
  figmaker.plot_WS_scatter(save_fig=True)
  


if __name__=='__main__':

  main()
