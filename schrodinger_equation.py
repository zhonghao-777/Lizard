import numpy as np
import scipy.constants as c

def deg_to_rad(deg):#define a function that converts degree to radian
    rad = np.pi*deg/180
    rad = round(rad,5)
    return rad
 
def rad_to_deg(rad):#define a function that converts radian to degree
    deg = 180*rad/np.pi
    deg = round(deg,5)
    return deg
    
def spherical_to_cartesian(r,theta,phi):#converts spherical coodinates to cartesian coordinates
    x = r*(np.sin(theta))*(np.cos(phi))
    y = r*(np.sin(theta))*(np.sin(phi))
    z = r*(np.cos(theta))
    
    x = round(x,5)
    y = round(y,5)
    z = round(z,5)
    
    ans = (x,y,z)
    return ans

def cartesian_to_spherical(x, y, z):#converts cartesian coordinates to spherical coordinates
    if x == 0 and y == 0:
        r = z
        theta = 0
        phi = 0
    
    else:
        r = (x**2 + y**2 + z**2)**0.5
        theta = np.arccos(z/r)
        phi = np.arccos(x/(x**2 + y**2)**0.5)
    
    r = round(r,5)
    theta = round(theta,5)
    phi = round(phi,5)
    
    ans = (r,theta,phi)
    return ans
    
def angular_wave_func(m,l,theta,phi):#calculate angular wave function
    pi = np.pi
    if l == 0 and m == 0:
        ans = (1/(4*pi))**0.5
    elif l == 1:
        if m == 1:
            ans = (-(3/(8*pi))**0.5)*(np.sin(theta))*(np.exp(np.complex(phi*1j)))
        elif m == 0:
            ans = ((3/(4*pi))**0.5)*(np.cos(theta))
        else:
            ans = ((3/(8*pi))**0.5)*(np.sin(theta))*(np.exp(np.complex(-phi*1j)))
    elif l == 2:
        if m == 2:
            ans = ((15/(32*pi))**0.5)*((np.sin(theta))**2)*(np.exp(np.complex(2*phi*1j)))
        elif m == 1:
            ans = ((-15/(8*pi))**0.5)*(np.cos(theta))*(np.sin(theta))*(np.exp(np.complex(phi*1j)))
        elif m == 0:
            ans = ((5/(16*pi))**0.5)*(3*(np.cos(theta))**2 - 1)
    
    ans = np.complex(round(ans,5))
    return ans
    
def radial_wave_func(n,l,r):#calculate radial wave function
    a=c.physical_constants['Bohr radius'][0]
    
    if n == 1 and l == 0:
        ans = ((2*(a**(-3/2)))*(np.exp(-r/a)))/(a**(-3/2))
    elif n == 2 and l == 1:
        ans = (1/(24**0.5))*((a)**(-3/2))*(r/a)*(np.exp(-r/(2*a)))/(a**(-3/2))
    elif n == 3 and l == 1:
        ans = (8/(27*(6**0.5)))*((a)**(-3/2))*(1-(r/(6*a)))*(r/a)*(np.exp(-r/(3*a)))/(a**(-3/2))
        
    ans = round(ans,5)
    return ans
    
    
def mgrid2d(xstart, xend, xpoints, ystart, yend, ypoints):
    xr = []
    yr = []
    xstep = (xend - xstart)/(xpoints - 1)
    ystep = (yend - ystart)/(ypoints - 1)
    
    xval = xstart
    xcount = 0
    
    while xcount < xpoints:
        
        yval = ystart
        ycount = 0
        xrow = []
        yrow = []
        
        while ycount < ypoints:
            
            xrow.append(xval)
            yrow.append(yval)
            yval += ystep
            ycount += 1
        
        xr.append(xrow)
        yr.append(yrow)
        xval += xstep
        xcount += 1
        
    return xr,yr
    
    
def mgrid3d(xstart, xend, xpoints, ystart, yend, ypoints, zstart, zend, zpoints):
    xr = []
    yr = []
    zr = []
    xval = xstart
    xcount = 0
    
    xstep = (xend - xstart)/(xpoints - 1)
    ystep = (yend - ystart)/(ypoints - 1)
    zstep = (zend - zstart)/(zpoints - 1)
    
    while xcount < xpoints:
        yval = ystart
        xrow = []
        yrow = []
        zrow = []
        ycount = 0
        
        while ycount < ypoints:
             zval = zstart
             xinner = []
             yinner = []
             zinner = []
             zcount = 0
             
             while zcount < zpoints:
                 xinner.append(xval)
                 yinner.append(yval)
                 zinner.append(zval)
                 zval += zstep
                 zcount += 1
             
             xrow.append(xinner)
             yrow.append(yinner)
             zrow.append(zinner)
             yval += ystep
             ycount += 1
             
        xr.append(xrow)
        yr.append(yrow)
        zr.append(zrow)
        xval += xstep
        xcount += 1
    return xr,yr,zr
    
    
def hydrogen_wave_func(n,l, m, roa, Nx, Ny, Nz):
    a=c.physical_constants['Bohr radius'][0]
    roundvec = np.vectorize(round)
    xx,yy,zz = np.array(mgrid3d(-roa, roa, Nx, -roa, roa, Ny, -roa, roa, Nz))
    cartesian_to_sphericalvec = np.vectorize(cartesian_to_spherical)
    r, theta, phi = cartesian_to_sphericalvec(xx,yy,zz)
    radial_wave_funcvec = np.vectorize(radial_wave_func)
    radial = radial_wave_funcvec(n,l,r*a)
    angular_wave_funcvec = np.vectorize(angular_wave_func)
    yp = angular_wave_funcvec(m,l,theta,phi)
    yn = angular_wave_funcvec(-m,l,theta,phi)
    if m < 0:
        Y = 1j/np.sqrt(2)*(yp-(-1)**m*yn)
    elif m > 0:
        Y = 1/np.sqrt(2)*(yn+(-1)**m*yp)
    else:
        Y = yp
    magni = (radial*abs(Y))**2
    return roundvec(xx,5),roundvec(yy,5),roundvec(zz,5),roundvec(magni,5)
