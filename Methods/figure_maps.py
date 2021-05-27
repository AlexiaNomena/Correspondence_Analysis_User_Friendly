import matplotlib
import matplotlib.pyplot as pl
import numpy as np
import scipy as scp
import pdb
import seaborn as sns

#### Extract elements to show on the maps ####
def Extract_specific(Labels, indicator, dtp):
    if indicator is None:
        Labels = np.array(Labels, dtype = dtp)
        specific = None
    else:
         sp = indicator
         #pdb.set_trace()
         specific = Labels == sp[0]
         for i in range(1,len(sp)):
             specific = specific + (Labels == sp[i])
         Labels = np.array(Labels[specific], dtype = dtp)
    return Labels, specific

def Extract_coordinates(Coords_dict, num_dim, Label_rows, Label_cols, special_row_cols):
    rows = Coords_dict["Full_rows"]
    cols = Coords_dict["Full_cols"]
    chosenAxes = Coords_dict["chosenAxes"]
    rows[:, chosenAxes] = Coords_dict["rows_in_fig"] # replace the values at the chosen axes because I sometimes flip or scale them in MCMCA the positions of the points
    cols[:, chosenAxes] = Coords_dict["cols_in_fig"]
    Label_rows, sp_rows = Extract_specific(Label_rows, special_row_cols[0], dtp = "int")
    Label_cols, sp_cols = Extract_specific(Label_cols, special_row_cols[1], dtp = "str")
    
    if sp_rows is None:
        xy_rows = rows[:, :num_dim]
    else:
        xy_rows = rows[sp_rows, :num_dim]
    
    if sp_cols is None:
        xy_cols = cols[:, :num_dim]
    else:
        xy_cols = cols[sp_cols, :num_dim]
    
    return xy_rows, xy_cols, Label_rows, Label_cols


#### Clustermaps ########       
    
def Clustering(data, colormap, labels_vert = None, labels_hor = None): 
    # Clustering using euclidean distance (for associating the same categorical variable: i.e. rows vs. rows or cols vs cols)    
    pdist_n = scp.spatial.distance.pdist(data)
    pdist = scp.spatial.distance.squareform(pdist_n)/np.amax(pdist_n) 
    
    cMap = sns.clustermap(pdist, method = "complete", cmap=colormap, 
                       yticklabels= labels_vert, xticklabels = labels_hor,
                       cbar_pos = (-0.1, 0.1, 0.03, 0.5),
                       cbar_kws = dict(ticks = (0, 0.5, 1), label = "Similarity")
                       )
    
    cax = cMap.cax
    #cax.set_yticks((0, 0.5, 1))
    cax.set_yticklabels(("high", "mid", "low"))
    
    return cMap 


def Clustering_rows_cols(Residuals, colormap, labels_vert = None, labels_hor = None): 
    # Clustering using distance from the origin and angle between vectors (for associating differenct categorical variables, i.e. rows vs. cols)
    # This means taking the dot products of the vectors
    """
    lrow = data_rows.shape[0]
    lcol = data_columns.shape[0]
    dist = np.zeros((lrow, lcol))
    
    for i in range(lrow):
        for j in range(lcol):
            dist[i, j] = data_rows[i, :].dot(data_columns[j,:])
    """
    #dist = data_rows.dot(data_columns.transpose()) # this has another meaning, see Greenacre 1993
    dist = Residuals
    
    
    # Normalization
    #negative = np.where(dist<0)[0][0]
    #positive = np.where(dist>=0)[0][0]
    
    #dist = dist*(negative*(1/np.amin(dist[negative])) + positive*(1/np.amax(dist[positive]))) # divide neg values with max of neg values and pos values with max of pos values
    #dist = dist/np.amax(dist)
    cMap = sns.clustermap(dist, method = "complete", cmap=colormap, 
                       yticklabels= labels_vert, xticklabels = labels_hor,
                       cbar_pos = (-0.15, 0.1, 0.03, 0.5),
                       cbar_kws = dict(ticks = (0, 0.25, 0.5, 0.75, 1), label = "Association")
                       )
    cax = cMap.cax
    #cax.set_yticks((0, 0.5, 1))
    cax.set_yticklabels(("none", "weak", "mid", "high", "high++"))
    
    return cMap     

def Clustering_rows_cols_fact(data_rows, data_columns, colormap, labels_vert = None, labels_hor = None): 
    # Clustering using distance from the origin and angle between vectors (for associating differenct categorical variables, i.e. rows vs. cols)
    # This means taking the dot products of the vectors
    """
    lrow = data_rows.shape[0]
    lcol = data_columns.shape[0]
    dist = np.zeros((lrow, lcol))
    
    for i in range(lrow):
        for j in range(lcol):
            dist[i, j] = data_rows[i, :].dot(data_columns[j,:])
    """
    dist = data_rows.dot(data_columns.transpose()) # this has another meaning, see Greenacre 1993
    #dist = Residuals
    
    
    # Normalization
    #negative = np.where(dist<0)[0][0]
    #positive = np.where(dist>=0)[0][0]
    
    #dist = dist*(negative*(1/np.amin(dist[negative])) + positive*(1/np.amax(dist[positive]))) # divide neg values with max of neg values and pos values with max of pos values
    dist = dist/np.amax(dist)
    cMap = sns.clustermap(dist, method = "complete", cmap=colormap, 
                       yticklabels= labels_vert, xticklabels = labels_hor,
                       cbar_pos = (-0.15, 0.1, 0.03, 0.5),
                       cbar_kws = dict(ticks = (0, 0.25, 0.5, 0.75, 1), label = "Association")
                       )
    cax = cMap.cax
    #cax.set_yticks((0, 0.5, 1))
    cax.set_yticklabels(("none", "weak", "mid", "high", "high++"))
    
    return cMap

def Clust_plot(cl_list, color, labels_vert, labels_hor, ticks_rotate, title, inrows = False):
    fig = pl.figure(figsize = (7,7))

    CMAP = Clustering(cl_list, colormap = color, labels_vert = labels_vert, labels_hor = labels_hor)
    
    # In case of other subplots to be added
    # set the gridspec to only cover half of the figure
    #CMAP.gs.update(left=0.05, right=0.45)
    
    #create new gridspec for the right part
    #gs2 = matplotlib.gridspec.GridSpec(1,1, left=0.6)
    # create axes within this new gridspec
    #ax2 = CMAP.fig.add_subplot(gs2[0])
    
    #ax2.axis("off")
    
    ax = CMAP.ax_heatmap
    # change axis params
    #ax.xaxis.tick_top() # x axis on top
    #ax.xaxis.set_label_position('top')
    
    if ticks_rotate[0]:
        for xticks in ax.get_xticklabels():
            xticks.set_rotation(90)
    
    if ticks_rotate[1]:
        for yticks in ax.get_yticklabels():
            yticks.set_rotation(0)
        
        
    pl.text(0, 1.65, title, fontsize = 16, bbox=dict(boxstyle='round,pad=0.2', fc="white", alpha=1))        
    ax.set_aspect("equal")
    return CMAP.fig 

def Clust_plot_rows_cols(data_rows, data_cols, color, labels_vert, labels_hor, ticks_rotate, title, inrows = False):
    fig = pl.figure(figsize = (7,7))

    CMAP = Clustering_rows_cols_fact(data_rows, data_cols, colormap = color, labels_vert = labels_vert, labels_hor = labels_hor)
    
    # In case of other subplots to be added
    # set the gridspec to only cover half of the figure
    #CMAP.gs.update(left=0.05, right=0.45)
    
    #create new gridspec for the right part
    #gs2 = matplotlib.gridspec.GridSpec(1,1, left=0.6)
    # create axes within this new gridspec
    #ax2 = CMAP.fig.add_subplot(gs2[0])
    
    #ax2.axis("off")
    
    ax = CMAP.ax_heatmap
    # change axis params
    #ax.xaxis.tick_top() # x axis on top
    #ax.xaxis.set_label_position('top')
    
    if ticks_rotate[0]:
        for xticks in ax.get_xticklabels():
            xticks.set_rotation(90)
    
    if ticks_rotate[1]:
        for yticks in ax.get_yticklabels():
            yticks.set_rotation(0)
        
        
    pl.text(0, 1.75, title, fontsize = 16, bbox=dict(boxstyle='round,pad=0.2', fc="white", alpha=1))        
    #ax.set_aspect("equal")
    return CMAP.fig 

def Axis_Clust_plots(cl, inds, labels_vert, labels_hor, tick_rotations, What, Loc, inrows = False):
    Figs = []
    for i in range(len(cl)):
        # Draw heatmap
        if i % 2 == 0:
            color = "Reds_r"
        else:
            color = "Greens_r"
        Figs.append(Clust_plot(cl[i], color, labels_vert[i][inds[i]], labels_hor[i][inds[i]], tick_rotations[i], 
                              title = "Clusters "+ What[i]+"\n"+"(%s)"%Loc[i]))
    return Figs    
      
def Cluster_maps(Coords_dict, form, Label_rows, Label_cols, standard, num_dim, specific_rows_cols = (None, None), axis_separation=True):
    xy_rows, xy_cols, Label_rows, Label_cols = Extract_coordinates(Coords_dict, num_dim, Label_rows, Label_cols, specific_rows_cols)
    
    if standard:
        print("Standart CA clustering")
        """
        In the case of standard CA, the axis must separate the clusters,
        Subclusters can then exist within the main clusters
        """
        
        #Residuals = Coords_dict["Residuals"]
        StandC = Coords_dict["Full_result"]["Coords_columns"]
        
        if specific_rows_cols[1] is None:
            Stand_columns = StandC[:, :num_dim]
        else:
            Stand_columns = StandC[specific_rows_cols[1], :num_dim]
    
        if axis_separation:
            labels_vert = [Label_cols, Label_rows, Label_cols, Label_rows]
            labels_hor = [Label_cols, Label_rows, Label_cols, Label_rows]
            tick_rotations = [(False, True),(True, False), (False, True), (True, False) ] # (xticks, yticks)
            What = ["Texts", form, "Texts", form]
            
            
            # Clusters separated by x-axis
            R1 = xy_rows[:, 1] > 0
            C1 = xy_cols[:, 1] > 0
            
            R2 = xy_rows[:, 1] < 0
            C2 = xy_cols[:, 1] < 0
            
            cl_x = [xy_cols[C1], xy_rows[R1], xy_cols[C2], xy_rows[R2]]
            Loc_x = ["upper", "upper", "lower","lower"]
            inds1 = [C1, R1, C2, R2]
            
            F_x = Axis_Clust_plots(cl_x, inds1, labels_vert, labels_hor, tick_rotations, What = What, Loc = Loc_x)
            
            
            # Rows and Cols together
            
            # divergingmap
            clmap = sns.color_palette("coolwarm")
            
            #RC_cl_upper = np.concatenate((xy_cols[C1], xy_rows[R1]), axis=0)
            #Residuals_upper = Residuals[R1, :][:, C1]
            Lab_vert = Label_rows[R1] #np.concatenate((Label_cols[C1], Label_rows[R1]))
            Lab_hor = Label_cols[C1] #np.concatenate((Label_cols[C1], Label_rows[R1]))
            
            #Lab_vert = np.concatenate((Label_cols[C1], Label_rows[R1]))
            #Lab_hor = np.concatenate((Label_cols[C1], Label_rows[R1]))
            
            C1_x =  [Clust_plot_rows_cols(xy_rows[R1], xy_cols[C1], clmap, Lab_vert, Lab_hor, (False,True), 
                                 title = "Clusterof texts and forms "+"\n"+"(Dim 2 upper) \n (fact dot fact)")]
            
            C1_x_b =  [Clust_plot_rows_cols(xy_rows[R1], Stand_columns[C1], clmap, Lab_vert, Lab_hor, (False,True), 
                                 title = "Clusterof texts and forms "+"\n"+"(Dim 2 upper) \n (fact dot stand)")]
            
            
            #RC_cl_lower = np.concatenate((Stand_columns[C2], xy_rows[R2]), axis=0)
            #Residuals_lower = Residuals[R2, :][:, C2]
            Lab_vert = Label_rows[R2] 
            Lab_hor = Label_cols[C2] 
            #Lab_vert = np.concatenate((Label_cols[C2], Label_rows[R2]))
            #Lab_hor = np.concatenate((Label_cols[C2], Label_rows[R2]))
            
            C2_x = [Clust_plot_rows_cols(xy_rows[R2], xy_cols[C2] , clmap, Lab_vert, Lab_hor, (False,True), 
                                 title = "Cluster of texts and forms "+"\n"+"(Dim 2 lower) \n (fact dot fact)")]
    
            C2_x_b = [Clust_plot_rows_cols(xy_rows[R2], Stand_columns[C2] , clmap, Lab_vert, Lab_hor, (False,True), 
                                 title = "Cluster of texts and forms "+"\n"+"(Dim 2 lower) \n (fact dot stand)")]
            
            # Clusters sperated by y-axis
            R3 = xy_rows[:, 0] > 0
            C3 = xy_cols[:, 0] > 0
             
            R4 = xy_rows[:, 0] < 0
            C4 = xy_cols[:, 0] < 0
            
            cl_y = [xy_cols[C3], xy_rows[R3], xy_cols[C4], xy_rows[R4]]
            Loc_y = ["right", "right", "left","left"] 
            inds2 = [C3, R3, C4, R4]
            
            F_y = Axis_Clust_plots(cl_y, inds2, labels_vert, labels_hor, tick_rotations, What = What, Loc = Loc_y)
            
            
            # Rows and Cols together
            #RC_cl_right = np.concatenate((Stand_columns[C3], xy_rows[R3]), axis=0)
            #Residuals_right = Residuals[R3, :][:, C3]
            Lab_vert = Label_rows[R3] #np.concatenate((Label_cols[C3], Label_rows[R3]))
            Lab_hor = Label_cols[C3] #np.concatenate((Label_cols[C3], Label_rows[R3]))
            
            #Lab_vert = np.concatenate((Label_cols[C3], Label_rows[R3]))
            #Lab_hor = np.concatenate((Label_cols[C3], Label_rows[R3]))
            
            
            C1_y =  [Clust_plot_rows_cols(xy_rows[R3], xy_cols[C3], clmap, Lab_vert, Lab_hor, (False,True), 
                                 title = "Cluster of texts and forms "+"\n"+"(Dim 1 right) \n (fact dot fact)")]
    
            C1_y_b =  [Clust_plot_rows_cols(xy_rows[R3], Stand_columns[C3], clmap, Lab_vert, Lab_hor, (False,True), 
                                 title = "Cluster of texts and forms "+"\n"+"(Dim 1 right) \n (fact dot stand)")]
            
            
            #RC_cl_left = np.concatenate((Stand_columns[C4], xy_rows[R4]), axis=0)
            #Residuals_left = Residuals[R4,  :][:, C4]
            Lab_vert = Label_rows[R4]
            Lab_hor = Label_cols[C4] 
            
            #Lab_vert = np.concatenate((Label_cols[C4], Label_rows[R4]))
            #Lab_hor = np.concatenate((Label_cols[C4], Label_rows[R4]))
            
            C2_y = [Clust_plot_rows_cols(xy_rows[R4], xy_cols[C4], clmap, Lab_vert, Lab_hor, (False,True), 
                                 title = "Cluster of texts and forms "+"\n"+"(Dim 1 left) \n (fact dot fact)")]
            
            C2_y_b = [Clust_plot_rows_cols(xy_rows[R4], Stand_columns[C4], clmap, Lab_vert, Lab_hor, (False,True), 
                                 title = "Cluster of texts and forms "+"\n"+"(Dim 1 left) \n (fact dot stand)")]
            
            Figs = C1_x + C1_x_b + C2_x + C2_x_b + C1_y + C1_y_b + C2_y + C2_y_b + F_x + F_y
        else:
            
            labels_vert = [Label_cols, Label_rows]
            labels_hor = [Label_cols, Label_rows]
            tick_rotations = [(False, True),(True, False)] # (xticks, yticks)
            What = ["Texts", form]
            
            
            # full cols
            sns.set(font_scale=0.7) # scale fontsize of labels
            F_1 = [Clust_plot(xy_cols, "Reds_r", Label_cols, Label_cols, ticks_rotate = (False, True), 
                              title = "Clusters of Text")]
            
            F_2 = [Clust_plot(xy_rows, "Greens_r", Label_rows, Label_rows, ticks_rotate = (False, True), 
                              title = "Clusters of forms")]
            
            # Rows and Cols together
            
            # divergingmap
            sns.set(font_scale=0.7)
            clmap = sns.color_palette("coolwarm")
            
            C_1 =  [Clust_plot_rows_cols(xy_rows, xy_cols, clmap, Label_rows, Label_cols, (False,True), 
                                 title = "Association between \n texts and forms) \n (fact dot fact)")]
    
            C_1_b = [Clust_plot_rows_cols(xy_rows, Stand_columns, clmap, Label_rows, Label_cols, (False,True), 
                                 title = "Association between \n texts and forms) \n (fact dot stand)")]
            
            # Euclidean proximity (removed because misleading)   
            """
            RC = np.concatenate((xy_cols, xy_rows), axis=0)
            Lab_vert = np.concatenate((Label_cols, Label_rows))
            Lab_hor = np.concatenate((Label_cols, Label_rows))
        
            C_2 = [Clust_plot(RC, "Blues_r", Lab_vert, Lab_hor, ticks_rotate = (False, True), 
                              title = "Clusters of \n Text and forms \n (fact dot fact)")]
            """
    
            Figs =  C_1 + C_1_b + F_1 + F_2 #+ C_2

    else:
        print("MCMCA clusters")
        Figs = []
        
        # Detailed dist separated Text and forms
        
        fig1 = Clust_plot(xy_cols, "Reds_r", Label_cols, Label_cols, ticks_rotate = (False, True), title = "Cluster Texts")
        
        sns.set(font_scale=0.7) # scale fontsize of labels

        thres = 100
        if xy_rows.shape[0] < thres: # one plot
            fig2 = Clust_plot(xy_rows, "Greens_r", Label_rows, Label_rows, ticks_rotate = (False, True), title = "Cluster "+form)
            
            RC = np.concatenate((xy_cols, xy_rows), axis=0)
            Lab_vert = np.concatenate((Label_cols, Label_rows))
            Lab_hor = np.concatenate((Label_cols, Label_rows))
            
            Figs.append(Clust_plot(RC, "Blues_r", Lab_vert, Lab_hor, ticks_rotate = (False, True), 
                              title = "Clusters of \n Text and forms"))
            Figs.append(fig1)
            Figs.append(fig2)
        else: # only plot the text cluster
            Figs.append(fig1) 
    
    return Figs 



#### Distance Heatmaps #####
"""
Unclustered result, not really needed anymore,
but in case it is needed, more work is necessary to update it
"""
def Compare_dist(axd, data, colormap, annot, labels_vert = None, labels_hor = None, symmetric = False):
    
    pdist_n = scp.spatial.distance.pdist(data)
    pdist = scp.spatial.distance.squareform(pdist_n)/np.amax(pdist_n)
    
    if symmetric:   
        # remove the lower or upper part
        mask = np.zeros_like(pdist, dtype=np.bool)
        mask[np.triu_indices_from(mask)] = True # upper part
        
        # remove the lower part instead, reverse the mask
        #mask = ~mask
        
        # Include diagonal elements as well
        mask[np.diag_indices_from(mask)] = False
        
        hMap = sns.heatmap(pdist, ax = axd, mask = mask, cmap=colormap, annot = annot, cbar = False, 
                           yticklabels= labels_vert, xticklabels = labels_hor, 
                           annot_kws={'fontweight':"bold", 'fontsize': "x-large"})
        
    else:
        hMap = sns.heatmap(pdist, ax = axd, cmap=colormap, annot = annot, cbar = False, 
                           yticklabels= labels_vert, xticklabels = labels_hor, 
                           annot_kws={'fontweight':"bold", 'fontsize': "x-large"})
        
  
    return hMap

def Dist_plot(cl_list, color, labels_vert, labels_hor, ticks_rotate, annot, sym, title, inrows = False):
    if inrows:
        # Define two rows for subplots
        fig, (ax, cax) = pl.subplots(nrows=2, figsize=(9.025,9.),  gridspec_kw={"height_ratios":[1,0.025]})
    else:
        # Define two cols for subplots
        fig, (ax, cax) = pl.subplots(ncols=2, figsize=(9.025,9.),  gridspec_kw={"width_ratios":[1,0.025]})
    
    Compare_dist(ax, cl_list, colormap = color, annot = annot, labels_vert = labels_vert, labels_hor = labels_hor, symmetric = sym)
    
    # change axis params
    #ax.xaxis.tick_top() # x axis on top
    #ax.xaxis.set_label_position('top')
    pl.suptitle(title, bbox=dict(boxstyle='round,pad=0.2', fc="white", alpha=1))      

    if ticks_rotate[0]:
        for xticks in ax.get_xticklabels():
            xticks.set_rotation(90)
    
    if ticks_rotate[1]:
        for yticks in ax.get_yticklabels():
            yticks.set_rotation(0)
    
    # colorbar
    if inrows:
        fig.colorbar(ax.get_children()[0], cax=cax, orientation="horizontal")
    else:
        fig.colorbar(ax.get_children()[0], cax=cax, orientation="vertical")
    
    return fig


def Axis_Dist_plots(cl, inds, labels_vert, labels_hor, tick_rotations, annotate, sym, What, Loc, inrows = False):
    Figs = []
    for i in range(len(cl)):
        # Draw heatmap
        if i % 2 == 0:
            color = "Reds_r"
        else:
            color = "Greens_r"
        Figs.append(Dist_plot(cl[i], color, labels_vert[i][inds[i]], labels_hor[i][inds[i]], tick_rotations[i], 
                             annot = annotate[i], sym = sym, title = "Distance between"+ What[i]+"\n"+" (%s)"%Loc[i]))
    return Figs
    
    
def Distance_maps(Coords_dict, form, Label_rows, Label_cols, standard, num_dim, specific_rows_cols = (None, None)):
    xy_rows, xy_cols, Label_rows, Label_cols = Extract_coordinates(Coords_dict, num_dim, Label_rows, Label_cols, specific_rows_cols)

    
    if standard:
        print("Standart CA distance matrix")
        """
        In the case of standard CA, the axis must separate the clusters,
        Subclusters can then exist within the main clusters
        """
    
        labels_vert = [Label_cols, Label_rows, Label_cols, Label_rows]
        labels_hor = [Label_cols, Label_rows, Label_cols, Label_rows]
        tick_rotations = [(False, True),(True, False), (False, True), (True, False) ] # (xticks, yticks)
        annotate = [True, False, True, False, True, False]
        What = ["Texts", form, "Texts", form]
        
        
        # Clusters separated by x-axis
        R1 = xy_rows[:, 1] > 0
        C1 = xy_cols[:, 1] > 0
        
        R2 = xy_rows[:, 1] < 0
        C2 = xy_cols[:, 1] < 0
        
        cl_x = [xy_cols[C1], xy_rows[R1], xy_cols[C2], xy_rows[R2]]
        Loc_x = ["upper", "upper", "lower","lower"]
        inds1 = [C1, R1, C2, R2]
        
        
        
        F_x = Axis_Dist_plots(cl_x, inds1, labels_vert, labels_hor, tick_rotations, annotate, sym = True, What = What, Loc = Loc_x)
        
        # Rows and Cols together
        RC_cl_upper = np.concatenate((xy_cols[C1], xy_rows[R1]), axis=0)
        
        Lab_vert = np.concatenate((Label_cols[C1], Label_rows[R1]))
        Lab_hor = np.concatenate((Label_cols[C1], Label_rows[R1]))
        
        
        C1_x = [Dist_plot(RC_cl_upper, "Blues_r", Lab_vert, Lab_hor, (True, False), 
                             annot = False, sym = True, title = "Distance between texts and forms \n"+"(Dim 2 upper)")]
        
        
        RC_cl_lower = np.concatenate((xy_cols[C2], xy_rows[R2]), axis=0)
        Lab_vert = np.concatenate((Label_cols[C2], Label_rows[R2]))
        Lab_hor = np.concatenate((Label_cols[C2], Label_rows[R2]))
        
        C2_x = [Dist_plot(RC_cl_lower, "Blues_r", Lab_vert, Lab_hor, (True, False), 
                             annot = False, sym = True, title = "Distance between texts and forms "+"\n"+"(Dim 2 lower)")]
    
        # Clusters sperated by y-axis
        R3 = xy_rows[:, 0] > 0
        C3 = xy_cols[:, 0] > 0
         
        R4 = xy_rows[:, 0] < 0
        C4 = xy_cols[:, 0] < 0
        
        cl_y = [xy_cols[C3], xy_rows[R3], xy_cols[C4], xy_rows[R4]]
        Loc_y = ["right", "right", "left","left"] 
        inds2 = [C3, R3, C4, R4]
        
        F_y = Axis_Dist_plots(cl_y, inds2, labels_vert, labels_hor, tick_rotations, annotate, sym = True, What = What, Loc = Loc_y)
        
        # Rows and Cols together
        RC_cl_right = np.concatenate((xy_cols[C3], xy_rows[R3]), axis=0)
        
        Lab_vert = np.concatenate((Label_cols[C3], Label_rows[R3]))
        Lab_hor = np.concatenate((Label_cols[C3], Label_rows[R3]))
        
        
        C1_y = [Dist_plot(RC_cl_right, "Blues_r", Lab_vert, Lab_hor, (True, False), 
                             annot = False, sym = True, title = "Distance between items \n"+"(Dim 1 right)")]
        
        
        RC_cl_left = np.concatenate((xy_cols[C4], xy_rows[R4]), axis=0)
        Lab_vert = np.concatenate((Label_cols[C4], Label_rows[R4]))
        Lab_hor = np.concatenate((Label_cols[C4], Label_rows[R4]))
        
        C2_y= [Dist_plot(RC_cl_left, "Blues_r", Lab_vert, Lab_hor, (True, False), 
                             annot = False, sym = True, title = "Distance between items"+"\n"+"(Dim 1 left)")]

        Figs = C1_x + C2_x + C1_y + C2_y + F_x + F_y
        
    else:
        print("MCMCA distances")
        Figs = []
        
        # Rows and Cols together
        # not possible because of the number of elements
        
        # Detailed dist separated Text and forms
        
        fig1 = Dist_plot(xy_cols, "Reds_r", Label_cols, Label_cols, ticks_rotate = (False, True), annot = True, sym = True, title = "Distance between Texts")
        Figs.append(fig1)
        
        thres = 100
        if xy_rows.shape[0] < thres: # one plot
            fig2 = Dist_plot(xy_rows, "Greens_r", Label_rows, Label_rows, ticks_rotate = (False, True), annot = False, sym = True, title = "Distance between"+form)
            Figs.append(fig2)
        
        
        
        """
        else: # several plots # not completed
            q,r = divmod(xy_rows.shape[0],thres)
    
            if r == 0:
                sections = [i*thres for i in range(q+1)]
            else:
                sections = [i*thres for i in range(q+1)]+[xy_rows.shape[0]]
            
            sections = np.array(sections, dtype = int)
            for i in range(len(sections)-1):
                start = sections[i]
                end = sections[i+1]
                fig2 = Dist_plot(xy_rows[start:end, :], "Greens_r", Label_rows[start:end], Label_rows[start:end], 
                                 ticks_rotate = (True, False), annot = False, sym = True, title = "Distance between "+form)
                Figs.append(fig2)
        """  
    
    return Figs
    
