import pandas as pd
import matplotlib.pyplot as plt
import matplotlib as mpl

# --------------------------------------------------------------
# Load data
# --------------------------------------------------------------
df = pd.read_pickle('../../data/interim/data_processed.pkl')

# --------------------------------------------------------------
# Plot single columns
# --------------------------------------------------------------
set_df = df[df['set']==1]
plt.plot(set_df['acc_y'].reset_index(drop=True))
# --------------------------------------------------------------
# Plot all exercises
# --------------------------------------------------------------

for label in df['label'].unique():
    subset = df[df['label']==label]
    fig,ax = plt.subplots()
    plt.plot(subset['acc_x'].reset_index(drop=True),label=label)
    plt.legend()
    plt.show()
    
for label in df['label'].unique():
    subset = df[df['label']==label]
    fig,ax = plt.subplots()
    plt.plot(subset[:100]['acc_x'].reset_index(drop=True),label=label)
    plt.legend()
    plt.show()

# --------------------------------------------------------------
# Adjust plot settings
# --------------------------------------------------------------

mpl.style.use('seaborn-v0_8-deep')
mpl.rcParams["figure.figsize"] = (20,5)
mpl.rcParams["figure.dpi"] = 100

# --------------------------------------------------------------
# Compare medium vs. heavy sets
# --------------------------------------------------------------

category_df = df.query("label == 'squat'").query("participant == 'A'").reset_index()

fig , ax = plt.subplots()
category_df.groupby(['category'])['acc_y'].plot()
ax.set_xlabel('Samples')
ax.set_ylabel('acc_y')
plt.legend()

# --------------------------------------------------------------
# Compare participants
# --------------------------------------------------------------

participants_df = df.query("label == 'bench'").sort_values('participant').reset_index()

fig , ax = plt.subplots()
participants_df.groupby(['participant'])['acc_y'].plot()
ax.set_xlabel('Samples')
ax.set_ylabel('acc_y')
plt.legend()



# --------------------------------------------------------------
# Plot multiple axis
# --------------------------------------------------------------

label = "squat"
participant = "A"
all_axis_df = df.query(f"label == '{label}'").query(f"participant == '{participant}'").reset_index()

fig , ax = plt.subplots()
all_axis_df[['acc_y','acc_x','acc_z']].plot(ax=ax)
ax.set_xlabel('Samples')
ax.set_ylabel('acc_y')
plt.legend()

# --------------------------------------------------------------
# Create a loop to plot all combinations per sensor
# --------------------------------------------------------------
for label in df['label'].unique():
    for participant in df['participant'].unique():
        all_axis_df = df.query(f"label == '{label}'").query(f"participant == '{participant}'").reset_index()
        
        if len(all_axis_df) > 0:

            fig , ax = plt.subplots()
            all_axis_df[['acc_y','acc_x','acc_z']].plot(ax=ax)
            ax.set_xlabel('Samples')
            ax.set_ylabel('acc_y')
            plt.title(f'{label} ({participant})'.title())
            plt.legend()

for label in df['label'].unique():
    for participant in df['participant'].unique():
        all_axis_df = df.query(f"label == '{label}'").query(f"participant == '{participant}'").reset_index()
        
        if len(all_axis_df) > 0:

            fig , ax = plt.subplots()
            all_axis_df[['gyr_y','gyr_x','gyr_z']].plot(ax=ax)
            ax.set_xlabel('Samples')
            ax.set_ylabel('gyr_y')
            plt.title(f'{label} ({participant})'.title())
            plt.legend()




# --------------------------------------------------------------
# Combine plots in one figure
# --------------------------------------------------------------
label = 'row'
participant = "A"
combined_plot_df = (
    df.query(f"label == '{label}'").query(f"participant == '{participant}'").reset_index(drop = True)
)

fig , ax = plt.subplots(nrows=2,sharex=True,figsize= (20,10))
combined_plot_df[['acc_y','acc_x','acc_z']].plot(ax=ax[0])
combined_plot_df[['gyr_y','gyr_x','gyr_z']].plot(ax=ax[1])

ax[0].legend(loc="upper center", bbox_to_anchor=(0.5, 1.15), ncol=3,fancybox=True,shadow=True)
ax[1].legend(loc="upper center", bbox_to_anchor=(0.5, 1.15), ncol=3,fancybox=True,shadow=True)
ax[1].set_xlabel('Samples')
# --------------------------------------------------------------
# Loop over all combinations and export for both sensors
# --------------------------------------------------------------
for label in df['label'].unique():
    for participant in df['participant'].unique():
        combined_plot_df = df.query(f"label == '{label}'").query(f"participant == '{participant}'").reset_index()
        
        if len(combined_plot_df) > 0:
            fig , ax = plt.subplots(nrows=2,sharex=True,figsize= (20,10))
            combined_plot_df[['acc_y','acc_x','acc_z']].plot(ax=ax[0])
            combined_plot_df[['gyr_y','gyr_x','gyr_z']].plot(ax=ax[1])

            ax[0].legend(loc="upper center", bbox_to_anchor=(0.5, 1.15), ncol=3,fancybox=True,shadow=True)
            ax[1].legend(loc="upper center", bbox_to_anchor=(0.5, 1.15), ncol=3,fancybox=True,shadow=True)
            ax[1].set_xlabel('Samples')
            plt.savefig(f"../../reports/figures/{label.title()}_{participant}.png")
            
            plt.show()